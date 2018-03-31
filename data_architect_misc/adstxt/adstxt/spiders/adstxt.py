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

    def __init__(self, category=None):
        # REF: https://stackoverflow.com/a/31242534
        self.create_output_dir()
        self.start_time = datetime.now().replace(microsecond=0)
        self.failed_urls = []

    def create_output_dir(self):
        cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.output_dir = os.path.join(cur_dir_path, datetime.now().strftime('%Y-%m-%d'))  # -%H%M%S'))
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    # TODO: replace thie method with loader for S3/Redshift
    def load_urls_to_crawl(self):
        cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        url_file = os.path.join(cur_dir_path, 'urls_to_scrape_all.csv')
        with open(url_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            return [b''.join(['https://', r[0], '/ads.txt']) for r in csvreader][0:10000]

    def start_requests(self):
        # urls = self.load_urls_to_crawl()
        urls = [
            # 'https://ES.EDUXDREAM.GHOST.DETECTOR/ads.txt', # DNSLookupError; catch it in err_callback() and store it in failure; it is NOT caught by process_spider_exception middleware
            #
            'https://www.coupons.com/ads.txt', # 404; caught by process_spider_exception middleware, so it'll now be captured in failure list
            # 'https://www.c-span.org/ads.txt', # 404
            # 'https://pages.ebay.com/ads.txt', # 404

            # 'https://YP.COM/ads.txt', # 301 error; following them gives you homepage or something totally different than expected. So i stopped redirect using meta. the error is caught by process_spider_exception middleware, so it'll now be captured in failure list
            # 'https://boomstreet.com/ads.txt' # same as above 302 redirect to either their https:// site or home page; do NOT follow and add them to failure list
            # 'https://freebiesfrenzy.com/ads.txt' # 302/301
            # 'https://ES-US.DEPORTES.YAHOO.COM/ads.txt' # 302/301

            # 'http://www.WSILTV.COM/ads.txt', # this works
            'https://www.WSILTV.COM/ads.txt',
            'http://www.WTOL.COM/ads.txt', # this works; SSL handshake error for 'https'; when exception happens, it doesn't go into 'parse()' nor 'process_spider_exception()' in the middleware, but it goes to err_callback
            # 'https://www.WSILTV.COM/random',

            # this returns SSL handshake error; retried 2-3 times and gave up; We need to use RetryMiddleWare to handle 'http', 'https' stuff
            # 'http://www.WTOL.COM/ads.txt', # this works; SSL handshake error for 'https'; when exception happens, it doesn't go into 'parse()' nor 'process_spider_exception()' in the middleware, but it goes to err_callback
            # 'http://www.WTOC.COM/ads.txt',  # SSL handshake error for 'https'
            # 'https://www.nbc12.com/ads.txt', # another SSL handshake failure
            # 'https://www.KTVN.COM/ads.txt', # another SSL handshake failure
            # 'https://www.KCBD.COM/ads.txt', # another SSL handshake failure
        ]
        for url in urls:
            meta = {
                'dont_redirect': True,
                # 'handle_httpstatus_list': [301, 302, 404, 500, 502], # if we add this, it'll follow redirect for these status codes
            }
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta=meta,
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
            return
        elif failure.check(DNSLookupError):
            # E.g., 'https://ES.EDUXDREAM.GHOST.DETECTOR/ads.txt' that does NOT exist or make any sense
            self.failed_urls.append([failure.request.url, 'DNSLookupError'])
            return
        elif failure.check(TimeoutError, TCPTimedOutError):
            # Not sure what we should do about them. Could be that the server was busy at the time.
            self.failed_urls.append([failure.request.url, 'TimeoutError'])
            return
        elif failure.check(ConnectionRefusedError):
            # return self.parse(scrapy.http.TextResponse(failure.request.url, status=222222))
            new_request = Request('http://www.WSILTV.COM/ads.txt', callback=self.parse, meta={'dont_redirect': True})
            self.crawler.engine.crawl(new_request, self.crawler.spider)
        else:
            pass

        return
        # if failure.value.reasons and ('OpenSSL.SSL.Error' in str(failure.value.reasons[0].type)):
        #     self.logger.error(repr(failure))
        #     self.logger.info('raising exception')

        # TODO: Add RetryMiddleware: https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.retry
