# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from scrapy.exporters import JsonItemExporter
import MySQLdb
# 这里必须提前导入 cursous
from MySQLdb import cursors
from twisted.enterprise import adbapi

"""
pipeline 主要用于数据存储
spider 中的每个 yield item 都会交给 item_pipeline 去处理，优先级根据后面的数字定义，越小优先级越高
item 类似于 dict 的模式
"""

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

# 自定义导出 json 文件
class JsonWithEncodingPipeline(object):
    def __init__(self):
        # 打开文件 codecs 能够避免很多编码的错误
        self.file = codecs.open("article.json", "w", encoding="utf-8")
    def process_item(self, item, spider):
        # 默认使用 ascii 编码，设置为 False 之后就关闭了默认的 ascii 编码
        lines = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

# 根据模块导出 json 文件
class JsonExporterPipeline(object):
    # 调用 scrapy 提供的 json export 导出 json 文件
    def __init__(self):
        self.file = open("articleexporter.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# 自定义 pipeline，继承 ImagesPipeline，设置 front_image_url 对应的 front_image_path
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item

# 插入数据库后好像不用 return item

# 同步写入数据库
# 解析速度大于数据的插入速度，导致阻塞
class Mysqlpipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect("127.0.0.1", "root", "123456", "jobbole", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article(title, create_time, url, url_object_id, front_image_url,
            front_image_path, praise_num, comm_num, fav_num, tags, content)
            values
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["create_time"], item["url"],
        item["url_object_id"], item["front_image_url"], item["front_image_path"],
        item["praise_num"], item["comm_num"], item["fav_num"], item["tags"], item["content"]))
        self.conn.commit()


# mysql 插入异步化
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # settings 就是 settings 文件中的值
    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = "utf8",
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        # twisted 本身只是个异步的容器，连接数据库还是德用 mysqldb 库
        # 第一个参数是连接的模块，后面是连接的参数
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用连接池做异步插入
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异步插入的异常
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    # 这里的 cursor 就是从 dbpool 拿出来的
    def do_insert(self, cursor, item):
        insert_sql = """
                    insert into article(title, create_time, url, url_object_id, front_image_url, front_image_path,
                    praise_num, comm_num, fav_num, tags, content)
                    values
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item["title"], item["create_time"], item["url"], item["url_object_id"],
                                    item["front_image_url"], item["front_image_path"], item["praise_num"],
                                    item["comm_num"], item["fav_num"], item["tags"], item["content"]))









