import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    page = 1
    start_urls = [f'https://www.labirint.ru/rating/?id_genre=-1&nrd=1&onpage=100']

    def parse(self, response: HtmlResponse):
        book_links = response.xpath("//a[@class='cover']/@href").extract()
        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        self.page += 1
        if self.page <= int(response.xpath('//div[@class="pagination-numbers"]/ul/li[last()]/a/text()').extract_first()):
            next_url = f'https://www.labirint.ru/rating/?id_genre=-1&nrd=1&onpage=100&page={self.page}'
            yield response.follow(next_url, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        href = response.url
        name = response.xpath('//div[@id="product-info"]/@data-name').extract_first()
        price = response.xpath('//div[@id="product-info"]/@data-price').extract_first()
        price_plus = response.xpath('//div[@id="product-info"]/@data-discount-price').extract_first()
        author = response.xpath('//div[@class="authors"]/a[@class="analytics-click-js"]/text()').extract_first()
        rating = response.xpath('//div[@id="rate"]/text()').extract_first()
        yield BookparserItem(name=name, href=href, price=price, price_plus=price_plus, author=author, rating=rating)
