import scrapy


class AldiSpiderSpider(scrapy.Spider):
    name = 'Aldi_Spider'
    allowed_domains = ['aldi.nl/producten.html']
    start_urls = ['http://aldi.nl/producten.html']

    def parse(self, response):
        for link in response.css('div.tiles-grid a::attr(href)'):
            yield response.follow('aldi.nl' + link.get(), callback=self.parse_categories)

    def parse_subcategories(self, response):
        for link in response.css('div.tiles-grid a::attr(href)'):
            yield response.follow('aldi.nl' + link.get(), callback=self.parse_products)

    def parse_products(self, response):
        for link in response.css('div.tiles-grid a::attr(href)'):
            yield response.follow('aldi.nl' + link.get(), callback=self.parse_data)

    def parse_data(self, response):
        datas = response.css('div.container')
        for data in datas:
            yield {
                'product_name': data.css('span.mod-article-intro__header-headline-small::text').get().strip(),
                'price': data.css('span.price__wrapper::text').get().strip(),
                'description': data.css('div.mod-article-intro__info::text').get().strip(),
            }
