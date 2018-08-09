# -*- coding: utf-8 -*-
import scrapy


class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    # 允许爬取的域名，如果不是这个域名将不会爬取
    allowed_domains = ['blog.jobbole.com']
    # 作为初始 url 生成 request，并默认把 parse 作为它的回调函数
    start_urls = ['http://blog.jobbole.com/110287']

    def parse(self, response):
        # //*[@id="post-110287"]/div[1]/h1
        re_selector = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract()[0]

        pass
