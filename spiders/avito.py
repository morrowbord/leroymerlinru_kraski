#leroymerlin parser
import scrapy
from scrapy.http import HtmlResponse
from items import AvitoparserItem
from scrapy.loader import ItemLoader


class AvitoSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self):
        self.start_urls = [
            # f'https://www.avito.ru/rossiya/bytovaya_elektronika?q={mark}']
            f'https://leroymerlin.ru/catalogue/kraski/']

    def parse(self, response: HtmlResponse):
        next_page = response.css(
            'a[data-qa-pagination-item="right"]::attr(href)').get()
        yield response.follow(next_page, callback=self.parse)

        ads_links = response.css(
            'a[data-qa="product-name"]::attr(href)').getall()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):

        name = response.css('h1.header-2::text').getall()
        photos = response.css('img[src]::attr(data-origin)').getall()
        price = response.css('span[slot="price"]::text').get()

        yield AvitoparserItem(name=name, photos=photos, price=price)

        print(name, photos, price)
