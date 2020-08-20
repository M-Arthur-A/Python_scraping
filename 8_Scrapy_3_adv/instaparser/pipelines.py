from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import scrapy
from urllib.parse import urlparse
import json
import os
import gc


class InstaparserPipeline:  # обработка items и подготовка к сохранению в БД
    def process_item(self, item, spider):
        if 'likes_data' in item.keys():
            item['likes_count'] = self.clear_likes(item['likes_data'])
            # запись в файл, для чтения его после скрапинга (файл check.py)
            if item['username'] == 'cg_boost':
                with open('temp_1.txt', 'a', newline='', encoding='UTF-8') as file_2:
                    file_2.writelines(['\n', str(item['likes_count'])])
            elif item['username'] == '_lena_volkova_':
                with open('temp_1.txt', 'a', newline='', encoding='UTF-8') as file_1:
                    file_1.writelines(['\n', str(item['likes_count'])])

        if 'followers_data' in item.keys():
            item['follower_data'] = self.clear_followers(item['followers_data'])

        if 'followings_data' in item.keys():
            item['following_data'] = self.clear_followings(item['followings_data'])
        return item

    def clear_likes(self, item):
        posts = item.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        res = 0
        for post in posts:
            res += int(post.get('node').get('edge_media_preview_like').get('count'))
        return res

    def clear_followers(self, item):
        followers = item.get('data').get('user').get('edge_followed_by').get('edges')
        res = []
        follower_data = {}
        for follower in followers:
            follower_data['id'] = follower.get('node').get('id')
            follower_data['name'] = follower.get('node').get('username')
            follower_data['fullname'] = follower.get('node').get('full_name')
            follower_data['avatar'] = follower.get('node').get('profile_pic_url')
            res.append(follower_data)
            follower_data = {}
        return res

    def clear_followings(self, item):
        followings = item.get('data').get('user').get('edge_follow').get('edges')
        res = []
        follow_data = {}
        for following in followings:
            follow_data['id'] = following.get('node').get('id')
            follow_data['name'] = following.get('node').get('username')
            follow_data['fullname'] = following.get('node').get('full_name')
            follow_data['avatar'] = following.get('node').get('profile_pic_url')
            res.append(follow_data)
            follow_data = {}
        return res


class InstaPhotosPipeline(ImagesPipeline):  # обработка фото и получение путей до них
    def get_media_requests(self, item, info):
        if 'follower_data' in item.keys():
            query = 'follower_data'
        elif 'following_data' in item.keys():
            query = 'following_data'

        if 'follower_data' in item.keys() or 'following_data' in item.keys():
            for i in item[query]:
                img = i['avatar']
                f_id = i['id']
                try:
                    yield scrapy.Request(img, meta={'folder': f_id + '/'})
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        file_true_name = os.path.basename(urlparse(request.url).path)
        return request.meta['folder'] + file_true_name

    def item_completed(self, results, item, info):
        if 'follower_data' in item.keys():
            query = 'follower_data'
        elif 'following_data' in item.keys():
            query = 'following_data'
        if 'follower_data' in item.keys() or 'following_data' in item.keys():
            for ind, i in enumerate(item[query]):
                if results[ind][0]:
                    if i['avatar'] == results[ind][1]['url']:
                        i['avatar'] = results[ind][1]
                    else:
                        for result in results:
                            if result[0]:
                                if result[1]['url'] == i['avatar']:
                                    i['avatar'] == result[1]
        return item


class InstaFinalizePipeline:  # сохранение в БД
    def process_item(self, item, spider):
        client = MongoClient('192.168.1.3', 27017)
        self.mongo_base = client.insta
        collection = self.mongo_base['profiles']
        if 'followers_data' in item.keys():
            del item['followers_data']
            collection.insert_one(item)
        if 'followings_data' in item.keys():
            del item['followings_data']
            collection.insert_one(item)
        return item

        # перебрать все items
        #
        # for obj in gc.get_objects():
        #     if isinstance(obj, scrapy.Item):
        #         print(obj)
