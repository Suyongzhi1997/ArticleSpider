# -*- coding: utf-8 -*-
import scrapy


class JoboleSpider(scrapy.Spider):
    name = 'jobole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/']

    def parse(self, response):
        pass
