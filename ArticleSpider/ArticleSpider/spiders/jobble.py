# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from urllib import parse


class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    # 允许爬取的域名，如果不是这个域名将不会爬取
    allowed_domains = ['blog.jobbole.com']
    # 作为初始 url 生成 request，并默认把 parse 作为它的回调函数
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中的 url 并交给 scrapy 下载
        2. scrapy 下载完成后交给 parse 函数进行解析

        """
        # 解析列表页中的所有文章 url 并交给 scrapy 下载后并进行解析
        post_urls = response.css("#archive .floated-thumb a.archive-title::attr(href)").extract()
        for post_url in post_urls:
            # 有时候获取的是路径，需要和域名进行拼凑
            # yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)
            yield Request(url=post_url, callback=self.parse_detail)

        # 提取下一页并交给 scrapy 进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url = next_url, callback=self.parse)

    def parse_detail(self, response):
        # 提取文章的具体字段
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
        pass
