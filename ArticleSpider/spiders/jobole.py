# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class JoboleSpider(scrapy.Spider):
    name = 'jobole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/kaifadou/snews-getajax.php?next=%d' % i for i in range(1, 3)]

    def parse(self, response):
        article_urls = response.xpath('//a/@href').extract()
        for article_url in article_urls:
            article_url = 'http://blog.jobbole.com' + article_url
            yield Request(url=article_url, callback=self.detail_parse)

    def detail_parse(self, response):
        title = response.xpath('//div[@class="main_left"]//h2/text()').extract_first()  # 新闻标题
        create_date = response.xpath('//div[@class="meta"]/span/text()').extract_first()  # 发布时间
        content = response.xpath('//div[@class="wen_article"]').extract_first()  # 文章正文
