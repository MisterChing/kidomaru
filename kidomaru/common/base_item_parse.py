# -*- coding: utf-8 -*-
import MySQLdb
import datetime
import time
import json
import hashlib
import os
import urllib
import sys
from kidomaru.conf.pool_config import *
from kidomaru.common.base_helper import *
from kidomaru.items import *
reload(sys)
sys.setdefaultencoding('utf8')

class BaseItemParse(object):

    @classmethod
    def parse_book_item(cls, response, rule_dict, filter_dict):
        s_item = BookItem()
        s_item['rule_dict'] = rule_dict
        s_item['filter_dict'] = filter_dict
        s_item['spider_id'] = response.meta['spider_id']
        s_item['is_check'] = response.meta['is_check']
        s_item['name'] = response.xpath(rule_dict['name']).extract()[0].strip()
        cover_url = response.xpath(rule_dict['cover']).extract()[0].strip()
        s_item['author'] = response.xpath(rule_dict['author']).extract()[0].strip()
        s_item['cover'] = saveImage(cover_url)
        if s_item['is_check'] > 0 and s_item['cover'] != '':    #更新最新章节最大id时 封面图片删除，节省空间
            os.remove(BASE_IMG_PATH + s_item['cover'])
        s_item['brief'] = response.xpath(rule_dict['brief']).extract()[0].strip()
        s_item['latest_chapter_url'] = response.xpath(rule_dict['latest_chapter_url']).extract()[0].strip()
        s_item['is_finish'] = 0
        s_item['cid'] = 1
        s_item['ctime'] = 0
        s_item['mtime'] = 0
        s_item['status'] = 1
        return s_item

    @classmethod
    def parse_volume_chapter_item(cls, response, rule_dict, filter_dict):
        item_list = response.xpath(rule_dict['chapter']).extract()
        return item_list

    @classmethod
    def parse_chapter_item(cls, response, rule_dict, filter_dict):
        s_item = ChapterItem()
        s_item['chapter_url'] = response.url
        s_item['rule_dict'] = rule_dict
        s_item['filter_dict'] = filter_dict
        s_item['spider_id'] = response.meta['spider_id']
        s_item['vid'] = 1
        s_item['bid'] = response.meta['bid']
        s_item['name'] = response.xpath(rule_dict['name']).extract()[0].strip()
        s_item['content'] = response.xpath(rule_dict['content']).extract()[0].strip()
        s_item['txt_count'] = 0
        s_item['ctime'] = 0
        s_item['mtime'] = 0
        s_item['status'] = 1
        return s_item

