# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from ArticleSpider.items import ArticleItem

from ArticleSpider.utils.common import get_md5


class JoboleSpider(scrapy.Spider):
    name = 'jobole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/kaifadou/snews-getajax.php?next=%d' % i for i in range(1, 3)]

    def parse(self, response):
        article_urls = response.xpath('//a/@href').extract()
        doc_img = ['http://blog.jobbole.com' + i for i in response.xpath('//div[@class="doc_img"]/img/@src').extract()]
        for article_url in article_urls:
            article_url = 'http://blog.jobbole.com' + article_url
            yield Request(url=article_url, meta={"doc_img": doc_img},
                          callback=self.detail_parse)

    def detail_parse(self, response):
        item = ArticleItem()
        item['url_object_id'] = get_md5(response.url)
        item['doc_img_url'] = response.meta.get('doc_img', '')  # 文章封面图
        item['title'] = response.xpath('//div[@class="main_left"]//h2/text()').extract_first()  # 新闻标题
        item['create_time'] = response.xpath('//div[@class="meta"]/span/text()').extract_first()  # 发布时间
        item['content'] = response.xpath('//div[@class="wen_article"]').extract_first()  # 文章正文
        yield item
