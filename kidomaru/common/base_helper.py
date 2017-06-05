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
reload(sys)
sys.setdefaultencoding('utf8')


def aa():
    print 'aaaaaaa'


def getSpiderList():
    conn = createMysql()
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    sql = "select * from `ci_novel_spider` where is_load=1 order by id desc"
    res = cursor.execute(sql)
    if res > 0:
        data = cursor.fetchall()
        result = [];
        for item in data:
            result.append(item)
        cursor.close()
        conn.close()
        return result
    else:
        cursor.close()
        conn.close()
        return


def createMysql():
    conn = MySQLdb.connect(user=DbConfig['dbuser'],
            passwd=DbConfig['dbpass'],
            db=DbConfig['dbname'],
            host=DbConfig['dbhost'],
            port=DbConfig['dbport'],
            charset=DbConfig['dbcharset']
            )
    return conn


def getGroupList():
    conn = createMysql()
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    sql = "select * from `ci_spider_group`"
    res = cursor.execute(sql)
    if res > 0:
        data = cursor.fetchall()
        result = {}
        for item in data:
            result[item['id']]= item
    else:
        result = None
    cursor.close()
    conn.close()
    return result

def getRuleList():
    conn = createMysql()
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    sql = "select * from `ci_spider_group`"
    res = cursor.execute(sql)
    if res > 0:
        data = cursor.fetchall()
        result = {}
        for item in data:
            result[item['id']] = item['rule']
        cursor.close()
        conn.close()
        return result
    else:
        cursor.close()
        conn.close()
        return

def getChapterByOrderId(order_id):
    conn = createMysql()
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    sql = "select * from ci_chapter where order_id=%d" % (order_id)
    res = cursor.execute(sql)
    if res > 0:
        return True
    else:
        return False
    cursor.close()
    conn.close()

def update_max_page(spider_id, max_page):
    conn = createMysql()
    cursor = conn.cursor()
    up_sql = "update `ci_novel_spider` set max_page=%d where id=%d" % (max_page, spider_id)
    cursor.execute(up_sql)
    conn.commit()
    cursor.close()
    conn.close()


def update_latest_chapter_url(spider_id, url):
    conn = createMysql()
    cursor = conn.cursor()
    up_sql = "update `ci_novel_spider` set latest_chapter_url='%s' where id=%d" % (url, spider_id)
    cursor.execute(up_sql)
    conn.commit()
    cursor.close()
    conn.close()

def update_recent_chapter_id(spider_id, order_id):
    conn = createMysql()
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    sql = "select recent_chapter_id from `ci_novel_spider` where id=%d" % (spider_id)
    res = cursor.execute(sql)
    if res > 0:
        data = cursor.fetchone()
        print 66666
        if order_id > data['recent_chapter_id']:
            up_sql = "update `ci_novel_spider` set recent_chapter_id=%d where id=%d" % (order_id, spider_id)
            cursor.execute(up_sql)
            conn.commit()
    cursor.close()
    conn.close()

def saveImage(img_url):
    base_path = BASE_IMG_PATH
    dynamic_path = time.strftime("%Y/%m/%d", time.localtime(time.time()))
    des_path = base_path + dynamic_path
    try:
        if not os.path.exists(des_path):
            os.makedirs(des_path)
        file_suffix = os.path.splitext(img_url)[1]
        file_name = createMD5(str(time.time()))
        full_path = des_path + '/' + file_name + file_suffix
        return_path = dynamic_path + '/' + file_name + file_suffix
        urllib.urlretrieve(img_url, filename=full_path)
        return return_path
    except IOError as e:
        print e
        return ''

def createMD5(str=''):
    m = hashlib.md5()
    m.update(str)
    new_str = m.hexdigest()
    return new_str

def format_url(base, tmp_url):
    pos = tmp_url.find(base)
    if pos == -1:
        new_url = base.strip('/') + '/' + tmp_url.strip('/')
        return new_url
    else:
        return tmp_url








