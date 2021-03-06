# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from urllib import parse
from ..items import JobBoleArticleItem, ArticleItemLoader
from ..utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader

class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    # 允许爬取的域名，如果不是这个域名将不会爬取
    allowed_domains = ['blog.jobbole.com']
    # 作为初始 url 生成 request，并默认把 parse 作为它的回调函数
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中的 url 并交给 scrapy 下载并进行解析
        2. scrapy 下载完成后交给 parse_detail 函数进行解析
        """
        # 解析列表页中的所有文章 url 并交给 scrapy 下载后并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            # 获取第一个元素，如果没有则默认为空
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            """
            如果没域名则拼凑, 如果有域名, 则忽略, 交给 scrapy 去下载，方便绝对路径和相对路径
            在列表页中获取的元素可以通过 meta 参数传递给下面的 response，所以可以通过这种方式获取列表页中的元素            
            """
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        # 提取下一页并交给 scrapy 进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            # 这里是文章列表页，继续调用 parse 函数
            yield Request(url = next_url, callback=self.parse)

    def parse_detail(self, response):

        item = JobBoleArticleItem()
        # 提取文章的具体字段

        # 获取上面传递过来的数据
        front_image_url = response.meta.get("front_image_url", "")

        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        create_time = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace('·', '').strip()
        praise_num = int(response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0])
        # class 为多值时，可以用 contain 函数
        fav_num = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(".*(\d)+.*", fav_num)
        fav_num = int(match_re.group(1)) if match_re else 0
        comm_num = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match(".*(\d)+.*", comm_num)
        comm_num = int(match_re.group(1)) if match_re else 0
        content = response.xpath("//div[@class='entry']").extract()[0]
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ','.join(tag_list)


        item["title"] = title
        item["url"] = response.url
        item["url_object_id"] = get_md5(response.url)
        item["comm_num"] = comm_num
        item["praise_num"] = praise_num
        item["fav_num"] = fav_num
        item["tags"] = tags
        item["content"] = content

        item["create_time"] = create_time
        # 有说要下载图片的 url 必须是列表形式
        # https://www.jianshu.com/p/e598d6d8170d
        item["front_image_url"] = [front_image_url]
        # 这样才能进入到 pipelines


        # 通过 ItemLoader 来加载 item, 能够实现解析与赋值同步
        front_image_url = response.meta.get("front_image_url", "")
        # item_loader = ItemLoader(item=JobBoleArticleItem, response=response)
        # 自定义的 loader, 继承 Itemloader
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_xpath("create_time", "//p[@class='entry-meta-hide-on-mobile']/text()")
        item_loader.add_xpath("praise_num", "//span[contains(@class, 'vote-post-up')]/h10/text()")
        item_loader.add_xpath("fav_num", "//span[contains(@class, 'bookmark-btn')]/text()")
        item_loader.add_xpath("comm_num", "//a[@href='#article-comment']/span/text()")
        item_loader.add_xpath("content", "//div[@class='entry']")
        item_loader.add_xpath("tags", "//p[@class='entry-meta-hide-on-mobile']/a/text()")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])

        # 最后必须要 load 才能生成 item
        article_item = item_loader.load_item()

        # 调用 yield 传递进 pipeline
        yield article_item
