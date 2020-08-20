import scrapy
from instaparser.items import InstaparserItem
from scrapy.http import HtmlResponse
import json
import re
from urllib.parse import urlencode
from copy import deepcopy


class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    users = ['_lena_volkova_', 'cg_boost']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    hashes = {
        'profile': 'd4d88dc1500312af6f937f7b804c68c3',
        'followers': 'c76146de99bb02f6415203be841dd25a',
        'following': 'd04b0a864b4b54837c0d870b0e77e076',
        'posts': 'bfa387b2992c3a52dcbe447467b4b771'
    }
    with open('/home/arthur/Project/GeekBrains/Python_scraping/!ADDS/hw8_adds/req.txt', 'r') as f:
        login_data = f.read().splitlines()
        insta_login = login_data[0]
        insta_pass = login_data[1]

    def parse(self, response: HtmlResponse):  # аутентификация (для направления запросов - не требуется)
        csrf_token = self.csrf_token(response.text)
        yield scrapy.FormRequest(
            self.login_url,
            method='POST',
            callback=self.users_parse,
            formdata={'username': self.insta_login,
                      'enc_password': self.insta_pass},
            headers={'X-CSRFToken': csrf_token}
        )

    def users_parse(self, response: HtmlResponse):  # запуск по каждому юзеру (при аутентификации метод - users_parse)
        j_data = response.json()
        if j_data['authenticated']:
        # csrf_token = self.csrf_token(response.text)
            for user in self.users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
                    # headers={'X-CSRFToken': csrf_token}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.id_user(response.text, username)
        variables = {'id': user_id, 'first': 12}

        # запускаем подсчет общего числа лайков user'а
        url_posts = f'{self.graphql_url}query_hash={self.hashes["posts"]}&{urlencode(variables)}'
        yield response.follow(
            url_posts,
            callback=self.likes_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

        # запускаем сбор данных о подписчиках
        variables['first'] = 24
        url_followers = f'{self.graphql_url}query_hash={self.hashes["followers"]}&{urlencode(variables)}'
        yield response.follow(
            url_followers,
            callback=self.followers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

        # запускаем сбор данных о подписках
        variables['first'] = 24
        url_followings = f'{self.graphql_url}query_hash={self.hashes["following"]}&{urlencode(variables)}'
        yield response.follow(
            url_followings,
            callback=self.followings_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def likes_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.graphql_url}query_hash={self.hashes["posts"]}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.likes_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        item = InstaparserItem(
            username=username,
            user_id=user_id,
            likes_data=j_data
        )
        yield item

    def followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_followers = f'{self.graphql_url}query_hash={self.hashes["followers"]}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        item = InstaparserItem(
            username=username,
            user_id=user_id,
            followers_data=j_data
        )
        yield item

    def followings_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_followings = f'{self.graphql_url}query_hash={self.hashes["following"]}&{urlencode(variables)}'
            yield response.follow(
                url_followings,
                callback=self.followings_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        item = InstaparserItem(
            username=username,
            user_id=user_id,
            followings_data=j_data
        )
        yield item

    def csrf_token(self, text):
        token = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return token.split(':').pop().replace(r'"', '')

    def id_user(self, text, username):
        Uid = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(Uid).get('id', username)
