from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from instaparser import settings
from instaparser.spiders.insta import InstaSpider
from pymongo import MongoClient

if __name__ == '__main__':
    settings_m = Settings()
    settings_m.setmodule(settings)
    process = CrawlerProcess(settings=settings_m)
    process.crawl(InstaSpider)
    process.start()
