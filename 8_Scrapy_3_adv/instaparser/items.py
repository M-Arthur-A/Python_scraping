import scrapy


class InstaparserItem(scrapy.Item):
    username = scrapy.Field()
    user_id = scrapy.Field()
    _id = scrapy.Field()
    ## не очищенные данные
    user_data = scrapy.Field()
    likes_data = scrapy.Field()
    followers_data = scrapy.Field()
    followings_data = scrapy.Field()
    likes_count = scrapy.Field()

    ## очищенные данные
    likes_total = scrapy.Field()  # всего лайков
    followers_count = scrapy.Field()  # всего подписчиков
    following_count = scrapy.Field()  # всего подписок
    follower_data = scrapy.Field()  # словарь о подписчике (имя, id, адрес до фото)
    following_data = scrapy.Field()  # словарь о подписке (имя, id, адрес до фото)
