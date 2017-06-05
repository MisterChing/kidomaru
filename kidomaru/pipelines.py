# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
import redis
import json
import logging
import sys
import warnings
import re
from kidomaru.conf.pool_config import *
from kidomaru.items import *
from kidomaru.common.base_helper import *
from twisted.enterprise import adbapi

class KidomaruPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(user=DbConfig['dbuser'],
                passwd=DbConfig['dbpass'],
                db=DbConfig['dbname'],
                host=DbConfig['dbhost'],
                port=DbConfig['dbport'],
                charset=DbConfig['dbcharset']
                )
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db=DbConfig['dbname'],
                user=DbConfig['dbuser'],
                passwd=DbConfig['dbpass'],
                cursorclass=MySQLdb.cursors.DictCursor,
                port=DbConfig['dbport'],
                charset=DbConfig['dbcharset']
                )

    def process_item(self, item, spider):
        itemList = ['BookItem','VolumeItem','ChapterItem']
        for insStr in itemList:
            itemIns = globals().get(insStr)
            if isinstance(item, itemIns):
                funcName = 'process' + insStr
                getattr(self, funcName)(item, spider)

    def processBookItem(self, item, spider):
        is_check = item['is_check']
        latest_chapter_id = item['latest_chapter_url'].split('/')[-1]
        latest_chapter_id = int(latest_chapter_id.replace('.html', ''))
        cursor = self.conn.cursor()
        if is_check > 0:    #更新原站最大章节id
            sql = "update ci_novel_spider set latest_chapter_id=%d where id=%d" % (latest_chapter_id, item['spider_id'])
            cursor.execute(sql)
            self.conn.commit()
        else:   #新增book
            sql = ("insert into `ci_book` set name='%s',author='%s',cover='%s',brief='%s',is_finish=%d,cid=%d,ctime=%d,mtime=%d,status=%d" %
                    (item['name'],item['author'],item['cover'],item['brief'],item['is_finish'],item['cid'],item['ctime'],item['mtime'],item['status'])
                    )
            st = cursor.execute(sql)
            if st > 0:
                insert_id = cursor.lastrowid
                self.conn.commit()
                #更新ci_nover_spider 表
                up_sql = "update `ci_novel_spider` set bid=%d where id=%d" % (insert_id, item['spider_id'])
                cursor.execute(up_sql)
                self.conn.commit()
        cursor.close()
        return item

    def processVolumeItem(self, item, spider):
        print type(item)
        print spider.name
        return item
        pass

    def processChapterItem(self, item, spider):
        order_id = item['chapter_url'].split('/')[-1]
        order_id = int(order_id.replace('.html', ''))
        conn = MySQLdb.connect(user=DbConfig['dbuser'],
                passwd=DbConfig['dbpass'],
                db=DbConfig['dbname'],
                host=DbConfig['dbhost'],
                port=DbConfig['dbport'],
                charset=DbConfig['dbcharset']
                )
        #  query = self.dbpool.runInteraction(self._do_insertChapter, item, spider)
        #  query.addErrback(self.handle_error)
        sql = ("insert into `ci_chapter` set vid=%d,bid=%d,name='%s',content='%s',txt_count=%d,order_id=%d,ctime=%d,mtime=%d,status=%d" %
                (item['vid'],item['bid'],item['name'],item['content'],item['txt_count'],order_id,item['ctime'],item['mtime'],item['status'])
                )
        cursor = conn.cursor()
        st = cursor.execute(sql)
        if st > 0:
            insert_id = cursor.lastrowid
            conn.commit()
            update_recent_chapter_id(item['spider_id'], order_id)
            # 写入redis
            mredis = redis.StrictRedis(REDIS_SERVER_IP, REDIS_SERVER_PORT)
            redisKey = 'book_order_' + str(item['bid'])
            mredis.zadd(redisKey, order_id, insert_id)
        cursor.close()
        conn.close()
        return item

    def handle_error(e):
        logging.error(e)

    def _do_insertChapter(self, conn, item, spider):
        sql = ("insert into `ci_chapter` set vid=%d,bid=%d,name='%s',content='%s',txt_count=%d,ctime=%d,mtime=%d,status=%d" %
                (item['vid'],item['bid'],item['name'],item['content'],item['txt_count'],item['ctime'],item['mtime'],item['status'])
                )
        print sql
        conn.execute(sql)



