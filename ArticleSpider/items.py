# -*- coding: utf-8 -*-

import scrapy
import datetime
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    create_time = value.split(' ')[0]
    try:
        create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d').date()
    except Exception as e:
        create_time = datetime.datetime.now().date()
    return create_time


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    content = scrapy.Field()
    # front_image_path = scrapy.Field()
