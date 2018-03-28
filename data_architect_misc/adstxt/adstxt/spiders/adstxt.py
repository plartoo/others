import scrapy
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
            'http://www.espn.com/ads.txt',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_ads_txt_line(self, ads_txt_str):
        field_names = ['exchange_name', 'exchange_id', 'payment_type', 'tag_id']
        return dict(zip(field_names, [i.strip() for i in ads_txt_str.split(AdsTxtSpider.DELIMITER)]))


    def parse(self, response):
        {
            'flag': 'With ads.txt',
            'domain': 'http://www.espn.com',
            'ads_txt_url': 'http://www.espn.com/ads.txt',
            'exchange_name': '# US/DOMESTIC VENDORS  and DEPORTES/SSLA\r'
        }
        {
            'flag': 'With ads.txt',
            'domain': 'http://www.espn.com',
            'ads_txt_url': 'http://www.espn.com/ads.txt',
            'exchange_name': 'google.com',
            'exchange_id': ' pub-7182528145592493',
            'seller_type': 'direct',
            'datetime_refreshed': '2018-03-27 22:45'
        }

        # out_dict['flag'] = "With ads.txt"
        # out_dict['domain'] = url
        # out_dict['ads_txt_url'] = transform_url_2
        # out_dict['exchange_name'] = it.split(',')[0]
        # out_dict['exchange_id'] = it.split(',')[1]
        # out_dict['seller_type'] = it.split(',')[2].split('#')[0].lower().strip()
        # out_dict['datetime_refreshed'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        # out_dict['comments'] = it.split('#')[1]
        # TODO: check response status and handle accordingly here
        ads_txt = []
        comment = ''
        cur_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        for line in response.body.split(b'\n'):
            line = line.decode('utf-8') # decode from str to bytes so that the carriage returns can be stripped away
            if line.startswith(AdsTxtSpider.COMMENT_CHAR):
                comment += line.strip()
            else:
                split_line = line.split(AdsTxtSpider.COMMENT_CHAR)
                comment += ''.join(split_line[1:]).strip()
                # TODO: revert to old conditional logic so that we don't record too much comment
                # TODO: try out with different sites below:
                # https://stackoverflow.com/ads.txt
                # https://www.reddit.com/ads.txt
                # https://weather.com/ads.txt

                pp.pprint(split_line[0])
                if split_line[0].strip():
                    ads_txt_dict = self.parse_ads_txt_line(split_line[0])
                    ads_txt_dict['has_adstxt'] = 1
                    # REF: https://stackoverflow.com/a/20728813
                    ads_txt_dict['domain'] = "{0.scheme}://{0.netloc}/".format(urlsplit(response.url))
                    ads_txt_dict['ads_txt_url'] = response.url
                    ads_txt_dict['last_fetched_date'] = cur_datetime
                    ads_txt_dict['comment'] = comment
                    ads_txt.append(ads_txt_dict)

        pp.pprint(ads_txt)
        # filename = 'adstxt-%s.txt' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
