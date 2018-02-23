import scrapy


class AdsTxtSpider(scrapy.Spider):
    name = "adstxt"

    def start_requests(self):
        urls = [
            'http://www.espn.com/ads.txt',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'adstxt-%s.txt' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
