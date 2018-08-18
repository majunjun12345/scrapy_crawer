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

# 虽然通过 loader 获取的是 列表，但是 value 是列表中的一个元素，MapCompose 对列表中的元素进行遍历处理
def date_convert(value):
    try:
        value = value.strip().replace('·', '').strip()
        create_time = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_time = datetime.datetime.now()
    return create_time

# 直接原来的值返回，覆盖默认的 first
def return_value(value):
    return value

# 去除不必要的元素
def remove_comment_tag(value):
    if "评论" in value:
        return ""
    else:
        return value

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


"""
input_processor 对传入的参数进行处理，对迭代器中的元素进行遍历处理
output_processor 对传出的参数进行过滤
"""

class JobBoleArticleItem(scrapy.Item):
    # 只有一种数据类型，相当于包含了所有类型
    title = scrapy.Field(
        # input_processor = MapCompose(add_jobbole)
        input_processor = MapCompose(lambda x:x+ "-jobbole")
    )
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert),
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
        input_processor=MapCompose(remove_comment_tag),
        output_processor=Join(",")
    )
    content = scrapy.Field()






# 可以使用插件像 django 的 model 那样：scrapy-djangoitem
# https://github.com/scrapy-plugins/scrapy-djangoitem