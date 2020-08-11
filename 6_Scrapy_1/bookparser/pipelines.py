# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class BookparserPipeline:
    def __init__(self):
        client = MongoClient('192.168.1.3', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        collection = self.mongo_base['books']
        if spider.name == 'book24ru':
            item = self.clear_txt(item)
        collection.insert_one(item)
        return item

    def clear_txt(self, item):
        # заполняем цену и цену со скидкой
        item['price'] = item['price'].replace(' р.', '')
        if not item['price']:
             item['price'] = item['price_plus']
             item['price_plus'] = None
        # приводим рейтинг к 10-балльной шкале
        item['rating'] = float(item['rating'].replace(',', '.')) / 5 * 10
        return item
