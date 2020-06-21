# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


class ArticlespiderPipeline:
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    """
    自定义json文件导出
    """

    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '123456', 'article_spider', charset='utf8', use_unicode=True)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into articles(title, create_time, content, url, url_object_id)
            values (%s, %s, %s, %s, %s)
        """
        self.cur.execute(insert_sql,
                         (item['title'], item['create_time'], item['content'], item['url'], item['url_object_id']))
        self.conn.commit()


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )

        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将mysql插入变成异步执行
        """
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)  # 处理异常

    def handle_error(self, failure):
        """
        处理异步插入的异常
        """
        print(failure)

    def do_insert(self, cur, item):
        insert_sql = """
                    insert into articles(title, create_time, content, url, url_object_id)
                    values (%s, %s, %s, %s, %s)
                """
        cur.execute(insert_sql,
                    (item['title'], item['create_time'], item['content'], item['url'], item['url_object_id']))


class JsonExportPipeline(object):
    """
    调用scrapy提供的json export导出json文件
    """

    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['front_image_path'] = image_file_path
        return item
