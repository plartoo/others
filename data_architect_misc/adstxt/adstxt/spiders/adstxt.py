import csv
import itertools
import os.path
from datetime import datetime
from urllib.parse import urlsplit
# import pprint
# pp = pprint.PrettyPrinter(indent=4)

import scrapy


class AdsTxtSpider(scrapy.Spider):
    name = "adstxt"
    COMMENT_CHAR = '#'
    DELIMITER = ','
    OUTPUT_DIR = None

    @classmethod
    def create_output_dir(cls):
        cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        cls.OUTPUT_DIR = os.path.join(cur_dir_path, datetime.now().strftime('%Y-%m-%d'))#-%H%M%S'))
        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR)

    # TODO: replace thie method with loader for S3/Redshift
    def load_urls_to_crawl(self):
        cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        url_file = os.path.join(cur_dir_path, 'urls_to_scrape.csv')
        with open(url_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            return [''.join(['https://',r[0],'/ads.txt']) for r in csvreader][0:10000]

    def start_requests(self):
        urls = self.load_urls_to_crawl()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

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
