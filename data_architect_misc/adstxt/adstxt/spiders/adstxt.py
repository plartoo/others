import scrapy
import csv
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)

from urllib.parse import urlsplit


class AdsTxtSpider(scrapy.Spider):
    name = "adstxt"
    COMMENT_CHAR = '#'
    DELIMITER = ','


    def start_requests(self):
        # TODO: plug in domain loader here
        urls = [
            # 'http://www.espn.com/ads.txt',
            # 'https://stackoverflow.com/ads.txt',
            # 'https://www.reddit.com/ads.txt',
            # 'https://weather.com/ads.txt',
            'https://HUFFINGTONPOST.COM/ads.txt'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_ads_txt_line(self, ads_txt_str):
        field_names = ['exchange_name', 'exchange_id', 'payment_type', 'tag_id']
        return dict(zip(field_names, [i.strip() for i in ads_txt_str.split(AdsTxtSpider.DELIMITER)]))


    def parse(self, response):
        # TODO: check response status and handle accordingly here
        # How to catch errors: https://doc.scrapy.org/en/latest/topics/request-response.html
        ads_txt_list = []
        cur_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        # import pdb
        # pdb.set_trace()
        for line in response.body.split(b'\n'):
            line = line.decode('utf-8') # decode from str to bytes so that the carriage returns can be stripped away
            if line.startswith(AdsTxtSpider.COMMENT_CHAR):
                comment = line.strip()
            elif AdsTxtSpider.COMMENT_CHAR in line:
                split_line = line.split(AdsTxtSpider.COMMENT_CHAR)
                comment = ''.join(split_line[1:]).strip()
            else:
                comment = ''
                # TODO: revert to old conditional logic so that we don't record too much comment

                # pp.pprint(split_line[0])
                if split_line[0].strip():
                    ads_txt_dict = self.parse_ads_txt_line(split_line[0])
                    ads_txt_dict['has_adstxt'] = 1
                    # REF: https://stackoverflow.com/a/20728813
                    ads_txt_dict['domain'] = "{0.scheme}://{0.netloc}/".format(urlsplit(response.url))
                    ads_txt_dict['ads_txt_url'] = response.url
                    ads_txt_dict['last_fetched_date'] = cur_datetime
                    ads_txt_dict['comment'] = comment
                    ads_txt_list.append(ads_txt_dict)
                    # To remove extra newlines here, REF: https://stackoverflow.com/q/39477662; bug report: https://github.com/scrapy/scrapy/issues/3034
                    yield ads_txt_dict


        # pp.pprint(ads_txt_list)
        # headers = ['exchange_name', 'exchange_id', 'payment_type', 'tag_id', 'has_adstxt', 'domain', 'ads_txt_url', 'last_fetched_date', 'comment']
        # filename = 'adstxt_output.csv'
        # with open(filename, 'w', newline='') as csvfile:
        #     csvwriter = csv.writer(csvfile, delimiter=',',
        #                             quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     csvwriter.writerow(headers)
        #     for r in ads_txt_list:
        #         csvwriter.writerow([
        #             r['exchange_name'],
        #             r['exchange_id'],
        #             r['payment_type'],
        #             r['tag_id'],
        #             r['has_adstxt'],
        #             r['domain'],
        #             r['ads_txt_url'],
        #             r['last_fetched_date'],
        #             r['comment']
        #         ])
        #
        # print("Finished")

#
# I
# am
# trying
# to
# scrape
# Ads.txt
# file
# from HuffingtonPost site
#
# using
# Scrapy(ver
# 1.5
# .0) with Python 3+ using code similar to below:
#
#
#     class AdsTxtSpider(scrapy.Spider):
#         name = "myspider"
#
#         def start_requests(self):
#             urls = [
#                 'https://HUFFINGTONPOST.COM/ads.txt'
#             ]
#             for url in urls:
#                 yield scrapy.Request(url=url, callback=self.parse)
#
#         def parse(self, response):
#             for line in response.body.split(b'\n'):
#                 line = line.decode('utf-8')
#                 yield {'content': line}
#
# But
# I
# get
# error
# below:
#
# 2018 - 03 - 28
# 15: 46:41[scrapy.core.scraper]
# ERROR: Error
# downloading < GET
# https: //
# www.huffingtonpost.com / ads.txt >
# Traceback(most
# recent
# call
# last):
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\site-p
# ackages\twisted\internet\defer.py
# ", line 1386, in _inlineCallbacks
# result = g.send(result)
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\site-p
# ackages\scrapy\core\downloader\middleware.py
# ", line 43, in process_request
# defer.returnValue((yield download_func(request=request, spider=spider)))
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\site-p
# ackages\twisted\internet\defer.py
# ", line 1363, in returnValue
# raise _DefGen_Return(val)
# twisted.internet.defer._DefGen_Return: < 403
# https: // www.huffingtonpost.com / ads.t
# xt >
#
# During
# handling
# of
# the
# above
# exception, another
# exception
# occurred:
#
# Traceback(most
# recent
# call
# last):
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\site-p
# ackages\twisted\internet\defer.py
# ", line 1386, in _inlineCallbacks
# result = g.send(result)
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\site-p
# ackages\scrapy\core\downloader\middleware.py
# ", line 53, in process_response
# spider = spider)
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\site-p
# ackages\scrapy\downloadermiddlewares\httpcompression.py
# ", line 39, in process_re
# sponse
# decoded_body = self._decode(response.body, encoding.lower())
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\site-p
# ackages\scrapy\downloadermiddlewares\httpcompression.py
# ", line 55, in _decode
# body = gunzip(body)
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\site-p
# ackages\scrapy\utils\gz.py
# ", line 37, in gunzip
# chunk = read1(f, 8196)
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\site-p
# ackages\scrapy\utils\gz.py
# ", line 24, in read1
# return gzf.read1(size)
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\gzip.p
# y
# ", line 289, in read1
# return self._buffer.read1(size)
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\_compr
# ession.py
# ", line 68, in readinto
# data = self.read(len(byte_view))
# File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\gzip.p
# y
# ", line 463, in read
# if not self._read_gzip_header():
#     File
# "c:\users\me\appdata\local\programs\python\python36-32\lib\gzip.p
# y
# ", line 411, in _read_gzip_header
# raise OSError('Not a gzipped file (%r)' % magic)
# OSError: Not
# a
# gzipped
# file(b'<?')
#
# If
# I
# From
# Google - ing, I
# ran
# into
# this
# thread