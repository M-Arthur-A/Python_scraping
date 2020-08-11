import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/knigi-bestsellery/']

    def parse(self, response: HtmlResponse):
        book_links = response.xpath("//a[contains(@class, 'book__image-link')]/@href").extract()
        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        next_page = response.xpath('//a[contains(@class, "catalog-pagination__item _text")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        href = response.url
        name = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//div[@class="item-actions__price-old"]/text()').extract_first()
        price_plus = response.xpath('//div[@class="item-actions__price"]/b/text()').extract_first()
        author = response.xpath('//a[@class="item-tab__chars-link"]/text()').extract_first()
        rating = response.xpath('//span[@class="rating__rate-value"]/text()').extract_first()
        yield BookparserItem(name=name, href=href, price=price, price_plus=price_plus, author=author, rating=rating)
