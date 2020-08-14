# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import scrapy
from urllib.parse import urlparse
import os


class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('192.168.1.6', 27017)
        self.mongo_base = client.doors

    def process_item(self, item, spider):
        item['params'] = self.zip_lists(item['params_name'], item['params_val'])
        del item['params_name'], item['params_val']
        collection = self.mongo_base['doors']
        collection.insert_one(item)
        return item

    def zip_lists(self, params, vals):
        return dict(zip(params, vals))


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        self.folder = item['_id'] + '/'
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        file_true_name = os.path.basename(urlparse(request.url).path)
        return self.folder + file_true_name

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
