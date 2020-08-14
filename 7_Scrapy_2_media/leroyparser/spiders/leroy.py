import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/mezhkomnatnye-dveri/']

    def parse(self, response: HtmlResponse):
        door_links = response.xpath('//a[@class="plp-item__info__title"]')
        for link in door_links:
            yield response.follow(link, callback=self.door_parse)

        next_page = response.xpath('//a[@class="paginator-button next-paginator-button"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def door_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('_id', '//span[@slot="article"]/text()')
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('photos', '//picture[@slot="pictures"]/img/@src')
        loader.add_xpath('params_name', '//dt/text()')
        loader.add_xpath('params_val', '//dd/text()')
        loader.add_value('href', response.url)
        loader.add_xpath('price', '//uc-pdp-price-view/span[1]/text()')
        yield loader.load_item()
