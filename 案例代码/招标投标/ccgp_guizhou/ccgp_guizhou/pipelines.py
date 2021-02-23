# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging


class CommonPipeline(object):

    def __init__(self, mongo_uri, mongo_db_name, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db_name = mongo_db_name
        self.mongo_collection = mongo_collection

        self.mongo_client = None
        self.mongo_db = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        在启动的时候调用，比 open_spider早
        该类方法用来从 Crawler 中初始化得到一个 pipeline 实例；它必须返回一个新的 pipeline 实例；
        Crawler 对象提供了访问所有 Scrapy 核心组件的接口，包括 settings 和 signals
        :param crawler:
        :return:
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGDB_URI'),
            mongo_db_name=crawler.settings.get('MONGDB_DB_NAME', 'db_trade'),
            mongo_collection=crawler.settings.get('MONGDB_COLLECTION', 't_trade_raw')
        )

    def open_spider(self, spider):
        """
        当 spider 被开启时，这个方法被调用。可以实现在爬虫开启时需要进行的操作，比如说打开一个待写入的文件，或者连接数据库等
        :param spider:
        :return:
        """
        try:
            self.mongo_client = pymongo.MongoClient(self.mongo_uri)
            self.mongo_db = self.mongo_client[self.mongo_db_name]
        except Exception as e:
            self.mongo_db = None
            logging.exception('init mongo db client failed')

    def close_spider(self, spider):
        """
        当 spider 被关闭时，这个方法被调用。可以实现在爬虫关闭时需要进行的操作，比如说关闭已经写好的文件，或者关闭与数据库的连接
        :param spider:
        :return:
        """
        self.mongo_client.close()

    def process_item(self, item, spider):
        """
        爬虫默认接口,处理item
        :param item:
        :param spider:
        :return:
        """
        # logging.debug('process_item {}'.format(dict(item)))
        try:
            self.mongo_db[self.mongo_collection].save(dict(item))
        except Exception as e:
            logging.exception('save item to mongodb failed')

        return item
