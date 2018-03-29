import itertools
from datetime import datetime
from urllib.parse import urlsplit
# import pprint
# pp = pprint.PrettyPrinter(indent=4)

import scrapy


class AdsTxtSpider(scrapy.Spider):
    name = "adstxt"
    COMMENT_CHAR = '#'
    DELIMITER = ','


    def start_requests(self):
        # TODO: check response status and handle accordingly
        # How to catch errors: https://doc.scrapy.org/en/latest/topics/request-response.html
        # https://stackoverflow.com/a/31149178
        # https://github.com/scrapy/scrapy/issues/2821
        # TODO: replace with method to load domains from csv here
        urls = [
            'http://www.espn.com/ads.txt',
            'https://stackoverflow.com/ads.txt',
            'https://www.reddit.com/ads.txt',
            'https://weather.com/ads.txt',
            'https://HUFFINGTONPOST.COM/ads.txt'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
                # , errback=self.err_callback)


    def parse_ads_txt_line(self, ads_txt_str):
        field_names = ['exchange_name', 'exchange_id', 'payment_type', 'tag_id']
        return dict(itertools.zip_longest(field_names, [i.strip() for i in ads_txt_str.split(AdsTxtSpider.DELIMITER)]))


    def parse(self, response):
        cur_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        for line in response.body.split(b'\n'):
            # Decode from str to bytes so that the carriage returns can be stripped away
            split_line = line.decode('utf-8').split(AdsTxtSpider.COMMENT_CHAR)
            comment = ''.join(split_line[1:]).strip()
            if split_line[0].strip():
                ads_txt_dict = self.parse_ads_txt_line(split_line[0])
                ads_txt_dict['has_adstxt'] = 1
                # REF: https://stackoverflow.com/a/20728813
                ads_txt_dict['domain'] = "{0.scheme}://{0.netloc}/".format(urlsplit(response.url))
                ads_txt_dict['ads_txt_url'] = response.url
                ads_txt_dict['last_fetched_date'] = cur_datetime
                ads_txt_dict['comment'] = comment
                yield ads_txt_dict
