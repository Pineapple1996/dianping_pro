# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import random


class DianpingProPipeline(object):
    def open_spider(self, spider):
        self.file_path = './data/{}.{}'.format(spider.name,random.randint(100,1000))
        self.file = open(self.file_path, "w")

    def process_item(self, item, spider):
        dictitem = dict(item)
        self.file.write(json.dumps(dictitem, ensure_ascii=False))
        self.file.write('\n')
        self.file.flush()
        return item

    def close_spider(self, spider):
        logging.info('存储数据成功，本地存储路径：{}'.format(self.file_path))
        self.file.close()
