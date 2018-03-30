# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import csv
import os.path
from datetime import datetime

from scrapy import signals


class AdstxtSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self):
        self.failed_URLs = []
        self.start_time = datetime.now().replace(microsecond=0)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        # REF: https://doc.scrapy.org/en/latest/topics/signals.html
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        # Should return None or raise an exception.
        # print(response.url, ':', response.status)
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        # How to catch exceptions REF: https://doc.scrapy.org/en/latest/topics/request-response.html
        # https://stackoverflow.com/a/31149178
        # https://github.com/scrapy/scrapy/issues/2821
        # print('exception:', response.url, ' =>', str(response.status))
        self.failed_URLs.append([response.url, response.status])
        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.create_output_dir()
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        output_file_name = ''.join(['failed_urls_', datetime.now().strftime('%Y-%m-%d'),'.csv'])
        output_file = os.path.join(spider.OUTPUT_DIR, output_file_name)
        # Note: we may not append and instead write new file; then aggregate them later
        with open(output_file, 'a', newline='', encoding='utf-8') as fo:
            try:
                writer = csv.writer(fo, delimiter=',', lineterminator='\n',
                                    quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writerows(self.failed_URLs)
                print('Recorded non-working URLs in file: ', output_file)
            except csv.Error as e:
                print('error', e)
                spider.logger.error('Error in writing CSV (output) file: ' + output_file)

        print('Total time taken:', str(datetime.now().replace(microsecond=0) - self.start_time))
        spider.logger.info('Spider closed: %s' % spider.name)


class AdstxtDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
