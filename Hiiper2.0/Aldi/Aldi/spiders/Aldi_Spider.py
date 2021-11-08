import scrapy
import json


class AldiSpiderSpider(scrapy.Spider):
    name = 'Aldi_Spider'
    allowed_domains = ['aldi.nl']
    start_urls = ['https://www.aldi.nl/producten.html']

    def parse(self, response):
        for link in response.css('.mod-content-tile__action::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_subcategories)

    def parse_subcategories(self, response):
        for link in response.css('.mod-content-tile__action::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_products)

    def parse_products(self, response):
        for link in response.css('.mod-article-tile__action::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_data)

    def parse_data(self, response):
        info1 = response.css(
            '.mod-article-title-intro::attr(data-article)')
        info2 = json.loads(info1)
        yield {
            'id': info2['productInfo']['productID'],
            'product_name': info2['productInfo']['productName'],
            'price': info2['productInfo']['priceWithTax'],
            'description': '',
            'url': info2['id'],
        }
