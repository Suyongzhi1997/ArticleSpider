# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy import Request
from scrapy.loader import ItemLoader

from ArticleSpider.items import ArticleItem, ArticleItemLoader

from ArticleSpider.utils.common import get_md5


class JoboleSpider(scrapy.Spider):
    name = 'jobole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/kaifadou/snews-getajax.php?next=%d' % i for i in range(1, 2)]

    def parse(self, response):
        article_urls = response.xpath('//a/@href').extract()
        for article_url in article_urls:
            article_url = 'http://blog.jobbole.com' + article_url
            yield Request(url=article_url, callback=self.detail_parse)

    def detail_parse(self, response):
        # item = ArticleItem()
        # item['url'] = response.url
        # item['url_object_id'] = get_md5(response.url)
        # item['title'] = response.xpath('//div[@class="main_left"]//h2/text()').extract_first()  # 新闻标题
        # create_time = response.xpath('//div[@class="meta"]/span/text()').extract_first()  # 发布时间
        # create_time = create_time.split(' ')[0]
        # try:
        #     create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d').date()
        # except Exception as e:
        #     create_time = datetime.datetime.now().date()
        # item['create_time'] = create_time
        # item['content'] = response.xpath('//div[@class="wen_article"]').extract_first()  # 文章正文

        #  通过item loader 加载item
        item_loader = ArticleItemLoader(item=ArticleItem(), response=response)
        item_loader.add_xpath('title', '//div[@class="main_left"]//h2/text()')
        item_loader.add_xpath('content', '//div[@class="wen_article"]')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_xpath('create_time', '//div[@class="meta"]/span/text()')
        article_loader = item_loader.load_item()
        yield article_loader
        # return item_loader.load_item()
        # yield item
