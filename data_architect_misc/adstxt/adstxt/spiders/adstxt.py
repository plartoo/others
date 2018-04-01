import csv
import itertools
import os.path
from datetime import datetime
from urllib.parse import urlsplit
# import pprint
# pp = pprint.PrettyPrinter(indent=4)

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.http import Request
from twisted.internet.error import DNSLookupError, ConnectionRefusedError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class AdsTxtSpider(scrapy.Spider):
    name = "adstxt"
    comment_char = b'#'
    delimiter = b','
    line_terminator = '\n'
    quote_char = '"'

    def __init__(self, start_index=None, *args, **kwargs):
        """
        Creates a Spider object instance.

        :param start_index: Optional index provided as commandline parameter
                            to start crawling from the list of URLs.
                            If not given, spider will scrap everything it loads
                            into the list of URLS.
        Note: num_to_crawl => if start_index is given, we'll crawl the next
                              10K URLs from there.
        """
        self.start_index = start_index
        self.num_to_crawl = 10000
        self.output_dir = self.get_output_dir()
        self.start_time = datetime.now().replace(microsecond=0)
        self.failed_urls = [] # Capture failed urls => REF: https://stackoverflow.com/a/31242534
        self.meta = {
                'dont_redirect': True,
                # if we add the key below, we will follow redirect for the status codes listed
                # 'handle_httpstatus_list': [301, 302, 404, 500, 502],
        }

    def get_output_dir(self):
        cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        output_dir = os.path.join(cur_dir_path, datetime.now().strftime('%Y-%m-%d'))  # -%H%M%S'))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    # TODO: replace thie method with loader for S3/Redshift
    def load_urls_to_crawl(self):
        cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        url_file = os.path.join(cur_dir_path, 'urls_to_scrape_all.csv')
        with open(url_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            return [''.join(['https://', r[0], '/ads.txt']) for r in csvreader]

    def start_requests(self):
        urls = self.load_urls_to_crawl()
        if self.start_index:
            index = int(self.start_index)
            assert index >= 0, "\n\n!!!Index provided in commandline must be non-negative.\n\n"
            urls = urls[index:(index+self.num_to_crawl)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta=self.meta,
                                 errback=self.err_callback)

    def parse_ads_txt_line(self, ads_txt_str):
        field_names = ['exchange_name', 'exchange_id', 'payment_type', 'tag_id']
        return dict(itertools.zip_longest(field_names, [i.strip() for i in ads_txt_str.split(AdsTxtSpider.delimiter)]))

    def parse(self, response):
        cur_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        # for sites like 'http://YP.COM/ads.txt' that redirects to 'https://YP.COM'
        # we added 'meta' in start_requests and we ignore response.status != 200
        for line in response.body.splitlines():
            # Decode from str to bytes so that the carriage returns can be stripped away
            # split_line = line.decode('utf-8').split(AdsTxtSpider.comment_char)
            split_line = line.split(AdsTxtSpider.comment_char)
            comment = b''.join(split_line[1:]).strip()
            if split_line[0].strip():
                ads_txt_dict = self.parse_ads_txt_line(split_line[0])
                ads_txt_dict['has_adstxt'] = 1
                # REF: https://stackoverflow.com/a/20728813
                ads_txt_dict['domain'] = "{0.scheme}://{0.netloc}/".format(urlsplit(response.url))
                ads_txt_dict['ads_txt_url'] = response.url
                ads_txt_dict['last_fetched_date'] = cur_datetime
                ads_txt_dict['comment'] = comment
                yield ads_txt_dict

    def err_callback(self, failure):
        # REF: https://doc.scrapy.org/en/latest/topics/request-response.html#using-errbacks-to-catch-exceptions-in-request-processing
        if failure.check(HttpError):
            # These exceptions come from HttpError spider middleware
            # you can get the non-200 response (404, 301, 302 etc.)
            # Note that we should not follow 301/302 because some sites
            # redirects us to their home pages and screws up our Ads.txt processing.
            # Also, we want to return as soon as we add them to failure url list;
            # otherwise, it'll go to middleware process_spider_exception().
            self.failed_urls.append([failure.value.response.url, failure.value.response.status])
        elif failure.check(DNSLookupError):
            # E.g., 'https://ES.EDUXDREAM.GHOST.DETECTOR/ads.txt' that does NOT exist or make any sense
            self.failed_urls.append([failure.request.url, 'DNSLookupError'])
        elif failure.check(TimeoutError, TCPTimedOutError):
            # Not sure what we should do about them. Could be that the server was busy at the time.
            self.failed_urls.append([failure.request.url, 'TimeoutError'])
        elif failure.check(ConnectionRefusedError):
            # This error is mostly because of SSL handshake error (http vs. https)
            if 'https' in failure.request.url:
                new_request = Request(failure.request.url.replace('https', 'http'),
                                      callback=self.parse, meta=self.meta)
                self.crawler.engine.crawl(new_request, self.crawler.spider)
                self.failed_urls.append([failure.request.url, 'Retrying http. Probably SSL handshake error.'])
            else:
                self.failed_urls.append([failure.request.url, str(failure.value)])
        else:
            self.failed_urls.append([failure.request.url, ''.join(['Unseen error: ', str(failure.value)])])

    def closed(self, reason):
        # REF: https://stackoverflow.com/a/33312325/1330974
        output_file_name = ''.join(['failed_urls_', datetime.now().strftime('%Y-%m-%d'),'.csv'])
        output_file = os.path.join(self.output_dir, output_file_name)

        with open(output_file, 'a', ) as fo:
            try:
                writer = csv.writer(fo,
                                    delimiter=self.delimiter.decode('utf-8'),
                                    lineterminator=self.line_terminator,
                                    quotechar=self.quote_char,
                                    quoting=csv.QUOTE_ALL)
                writer.writerows(self.failed_urls)
                self.logger.info('Recorded non-working URLs in file: ' + output_file)
            except csv.Error as e:
                self.logger.error('Error in writing CSV (output) file: ' + output_file)
                self.logger.error(str(e))

        self.logger.info('\n\n:::::> Total time taken: ' +
                         str(datetime.now().replace(microsecond=0) - self.start_time) +
                         '\n\n')

