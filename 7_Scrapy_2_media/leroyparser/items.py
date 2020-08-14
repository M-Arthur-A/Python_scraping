# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def cleaner_txt(txt):
    txt = txt.replace('\n', '')  # удаление переноса строки
    txt = ''.join(txt.split('  ')).strip()  # удаление двойных пробелов
    return txt


def get_int_value(value):
    return int(''.join(i for i in value[0] if i.isdigit()))


def get_id(txt):
    return txt.replace('Арт. ', '').strip()


class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field(input_processor=MapCompose(get_id), output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    params_name = scrapy.Field()
    params_val = scrapy.Field(input_processor=MapCompose(cleaner_txt))
    params = scrapy.Field()
    href = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=get_int_value)
