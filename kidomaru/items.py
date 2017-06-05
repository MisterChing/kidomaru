# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KidomaruItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    spider_id = scrapy.Field()
    is_check = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    cover = scrapy.Field()
    brief = scrapy.Field()
    is_finish = scrapy.Field()
    cid = scrapy.Field()
    ctime = scrapy.Field()
    mtime = scrapy.Field()
    status = scrapy.Field()
    page_url = scrapy.Field()
    latest_chapter_url = scrapy.Field()
    latest_chapter_time = scrapy.Field()
    rule_dict = scrapy.Field()
    filter_dict = scrapy.Field()

class VolumeItem(scrapy.Item):
    name = scrapy.Field()
    bid = scrapy.Field()

class ChapterItem(scrapy.Item):
    chapter_url = scrapy.Field()
    spider_id = scrapy.Field()
    vid = scrapy.Field()
    bid = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    txt_count = scrapy.Field()
    ctime = scrapy.Field()
    mtime = scrapy.Field()
    status = scrapy.Field()
    rule_dict = scrapy.Field()
    filter_dict = scrapy.Field()
