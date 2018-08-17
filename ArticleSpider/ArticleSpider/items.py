# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_jobbole(value):
    return value + "-jobbole"

class JobBoleArticleItem(scrapy.Item):
    # 只有一种数据类型，相当于包含了所有类型
    title = scrapy.Field(
        # input_processor = MapCompose(add_jobbole)
        input_processor = MapCompose(lambda x:x+ "-jobbole")
    )
    create_time = scrapy.Field()
    url = scrapy.Field()
    # url 是变长的，通过 md5 将其变为定长
    url_object_id = scrapy.Field()

    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_num = scrapy.Field()
    comm_num = scrapy.Field()
    fav_num = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()






# 可以使用插件像 django 的 model 那样：scrapy-djangoitem
# https://github.com/scrapy-plugins/scrapy-djangoitem