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

        data = response.css('span.price__unit::text').get().strip()

        new_data = ''.join((ch if ch in 'abcdefghijklmnoupPqrstvxyz' else ' ')
                           for ch in data)
        amount1 = [i for i in new_data.split()]

        new_data2 = ''.join((ch if ch in '1234567890x/' else ' ')
                            for ch in data)
        quantity1 = [i for i in new_data2.split()]

        price1 = info2['productInfo']['priceWithTax']
        if(price1 == -1.0):
            price1 = "Out of Stock"

        description1 = response.css('.rte > p::text').get()
        if(description1 == "Ondanks zorgvuldige planning kan het voorkomen dat actie-artikelen door de grote vraag snel zijn uitverkocht. Mochten de actie-artikelen sneller uitverkocht zijn dan voorzien, dan vragen wij hiervoor begrip. Er geldt maximaal 4 dezelfde (non-food) aanbiedingen per klant per bezoek. De afgebeelde artikelen kunnen afwijken van de werkelijkheid." or description1 == "U ontvangt van ons een e-mail om uw e-mailadres te bevestigen. Klik op de link in de e-mail."):
            description1 = "No Description"

        yield {
            'shop': 'Aldi',
            'product_id': info2['productInfo']['productID'],
            'product_name': info2['productInfo']['productName'],
            'price': price1,
            'description': description1,
            'images': response.css('a.mod-gallery-article__media::attr(href)').get(),
            'category_level_1': info2['productCategory']['primaryCategory'],
            'category_level_2': info2['productCategory']['subCategory1'],
            'quantity': quantity1[0],
            'amount': amount1[0],
            'url': response.url,
            'date': today1,
            'time': time1,
        }
