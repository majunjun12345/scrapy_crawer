# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobBoleArticleItem(scrapy.Item):
    # 只有一种数据类型，相当于包含了所有类型
    title = scrapy.Field()
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