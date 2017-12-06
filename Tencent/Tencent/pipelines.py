# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from Tencent.items import TencentItem, PositionItem
import json

class TencentJsonPipeline(object):
    def open_spider(self, spider):
        self.filename = open("tencent.json", "w")

    def process_item(self, item, spider):
        if isinstance(item, TencentItem):
            content = json.dumps(dict(item)) + ",\n"
            self.filename.write(content)
        return item

    def close_spider(self, spider):
        self.filename.close()


class PositionJsonPipeline(object):
    def open_spider(self, spider):
        self.filename = open("position.json", "w")

    def process_item(self, item, spider):
        if isinstance(item, PositionItem):
            content = json.dumps(dict(item)) + ",\n"
            self.filename.write(content)
        return item

    def close_spider(self, spider):
        self.filename.close()
