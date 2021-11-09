import scrapy
import json
import datetime


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
        info1 = response.css('.mod-article-intro::attr(data-article)').get()
        info2 = json.loads(info1)
        today1 = datetime.datetime.now().strftime("%x")
        time1 = datetime.datetime.now().strftime("%X")

        yield {
            'shop': 'Aldi',
            'product_id': info2['productInfo']['productID'],
            'product_name': info2['productInfo']['productName'],
            'price': info2['productInfo']['priceWithTax'],
            'description': '',
            'images': '',
            'category_level_1': info2['productCategory']['primaryCategory'],
            'category_level_2': info2['productCategory']['subCategory1'],
            'quantity': response.css('span.price__unit::text').get().strip(),
            'amount': '',
            'url': 'aldi.nl' + info2['id'],
            'date': today1,
            'time': time1,
        }
