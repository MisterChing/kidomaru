# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
import json
import logging
import sys
import warnings
import re
from scrapy.exceptions import DropItem
from kidomaru.conf.pool_config import *
from kidomaru.items import *

class NovelFilterItem(object):

    def process_item(self, item, spider):
        itemList = ['BookItem','VolumeItem','ChapterItem']
        for insStr in itemList:
            itemIns = globals().get(insStr)
            if isinstance(item, itemIns):
                funcName = 'filter' + insStr
                item = getattr(self, funcName)(item, spider)
                return item

    def filterBookItem(self, item, spider):
        filter_dict = item['filter_dict']
        if filter_dict.has_key('name') and filter_dict['name']:
            item['name'] = re.sub(filter_dict['name'].decode(), '', item['name'])
            item['name'] = item['name'].strip()
        if filter_dict.has_key('author') and filter_dict['author']:
            item['author'] = re.sub(filter_dict['author'].decode(), '', item['author'])
            item['author'] = item['author'].strip()
        if filter_dict.has_key('brief') and filter_dict['brief']:
            item['brief'] = re.sub(filter_dict['brief'].decode(), '', item['brief'])
            item['brief'] = item['brief'].strip()
        return item

    def filterVolumeItem(self, item, spider):
        print type(item)
        print spider.name
        return item
        pass

    def filterChapterItem(self, item, spider):
        filter_dict = item['filter_dict']
        if filter_dict.has_key('name') and filter_dict['name']:
            item['name'] = re.sub(filter_dict['name'].decode(), '', item['name'])
            item['name'] = item['name'].strip()
        if filter_dict.has_key('content') and filter_dict['content']:
            for tmp_rule in filter_dict['content']:
                item['content'] = re.sub(tmp_rule.decode(), '', item['content'])
            item['content'] = item['content'].strip()
        return item

