import scrapy


class AldiSpiderSpider(scrapy.Spider):
    name = 'Aldi_Spider'
    allowed_domains = ['aldi.nl/producten.html']
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
        datas = response.css('div.container')
        for data in datas:
            yield {
                'product_name': '',
                'price': data.css('span.price__wrapper::text').get().strip(),
                'description': '',
            }
