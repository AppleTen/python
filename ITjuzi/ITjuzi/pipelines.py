# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

class ItjuziPipeline(object):
    def process_item(self, item, spider):
        item['source'] = spider.name
        item['utc_time']  = str(datetime.utcnow())
        return item
