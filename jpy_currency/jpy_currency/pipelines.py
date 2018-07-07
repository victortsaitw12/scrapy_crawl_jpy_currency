# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from jpy_currency.utility import Utility 
from scrapy.conf import settings

class CurrencyPipeline(object):

    def process_item(self, item, spider):
        print 'process item:%s' % dict(item)
        item['jpy'] = float(item['jpy'])
        db = Utility.getDB()
        db[settings['MONGO_COLLECTION']].insert_one(dict(item))
        return item
