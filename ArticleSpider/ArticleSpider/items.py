# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
import re


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def get_nums(value):
    match_re = re.match(".*(\d)+.*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

def add_jobbole(value):
    return value + "-jobbole"

def date_convert(value):
    try:
        create_time = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_time = datetime.datetime.now()
    return create_time

def return_value(value):
    return value

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    # 只有一种数据类型，相当于包含了所有类型
    title = scrapy.Field(
        # input_processor = MapCompose(add_jobbole)
        input_processor = MapCompose(lambda x:x+ "-jobbole")
    )
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert),
        output_processor=TakeFirst()
    )
    url = scrapy.Field()
    # url 是变长的，通过 md5 将其变为定长
    url_object_id = scrapy.Field()

    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comm_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        output_processor=Join(",")
    )
    content = scrapy.Field()






# 可以使用插件像 django 的 model 那样：scrapy-djangoitem
# https://github.com/scrapy-plugins/scrapy-djangoitem