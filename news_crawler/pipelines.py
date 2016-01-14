# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.collection_name = 'articles'
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        #self.db.profiles.create_index([('url', pymongo.ASCENDING)], unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if "texto" in item and "categoria" in item:
            self.db[self.collection_name].update({'url': item['url']}, dict(item), upsert=True)
            return item
        else:
            raise DropItem("Faltando categoria em %s" % item)


class NewsCrawlerPipeline(object):

    def process_item(self, item, spider):
        return item
