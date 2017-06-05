import scrapy
from kidomaru.common.base_helper import *
from kidomaru.common.base_phantomjs import *
from kidomaru.common.base_item_parse import *
from kidomaru.items import *
import re

class TestSpider(scrapy.Spider):
    name = 'test'

    def __init__(self):
        self.spiderGroup = getGroupList()

    def start_requests(self):
        spiderList = getSpiderList()
        for item in spiderList:
            s_group = self.spiderGroup[item['gid']]
            bookRule = json.loads(s_group['rule'])['book']
            if item['bid'] > 0:
                meta = {
                        'timeout':10,
                        'bid':item['bid'],
                        'gid':item['gid'],
                        'noImage':True,
                        'spider_id':item['id'],
                        'has_volume':bookRule['has_volume'],
                        'is_catalog_paging':bookRule['is_catalog_paging'],
                        'latest_chapter_url':item['latest_chapter_url'],
                        'latest_chapter_id':item['latest_chapter_id']
                        }
                if bookRule['is_js_render'] == True:
                    meta['PhantomJs'] = True
                #  page_url = item['page_url']
                #  page_rule = self.ruleGroup[item['gid']]
                #  page_rule = json.loads(page_rule)
                #  page_rule = page_rule['book']['page_replace']
                #  next_page = re.sub(page_rule['from'], page_rule['to'] + str(next_symbol), page_url)
                next_page = item['catalog_url']
                #  if item['recent_chapter_id'] != item['latest_chapter_id']:
                yield scrapy.Request(next_page, meta=meta, callback=self.parse_volume)
            else:
                meta = {
                        'timeout':10,
                        'gid':item['gid'],
                        'spider_id':item['id'],
                        'is_check':item['is_check']
                        }
                if bookRule['is_js_render'] == True:
                    meta['PhantomJs'] = True
                yield scrapy.Request(url=item['url'], meta=meta, callback=self.parse_book)

    def parse_book(self, response):
        gid = response.meta['gid']
        s_group = self.spiderGroup[gid]
        bookRule = json.loads(s_group['rule'])['book']
        if s_group['filter'].strip():
            bookFilter = json.loads(s_group['filter'])['book']
        else:
            bookFilter = {}
        item = BaseItemParse.parse_book_item(response, bookRule, bookFilter)
        yield item

    def parse_volume(self, response):
        gid = response.meta['gid']
        bid = response.meta['bid']
        spider_id = response.meta['spider_id']
        latest_chapter_url = response.meta['latest_chapter_url']
        s_group = self.spiderGroup[gid]
        bookRule = json.loads(s_group['rule'])['book']
        volumeRule = json.loads(s_group['rule'])['volume']
        if s_group['filter'].strip():
            volumeFilter = json.loads(s_group['filter'])['volume']
        else:
            volumeFilter = {}
        itemList = BaseItemParse.parse_volume_chapter_item(response, volumeRule, volumeFilter)
        #  m = re.search(r'(\d+)\.html', latest_chapter_url)
        #  if m:
            #  latest_chapter_id = int(m.group(1))
        #  else:
            #  latest_chapter_id = 0
        new_itemList = []
        for tmpUrl in itemList:
            tmp_chapter_id = tmpUrl.split('/')[-1]
            tmp_chapter_id = int(tmp_chapter_id.replace('.html', ''))
            tmp_exists = getChapterByOrderId(tmp_chapter_id)
            if not tmp_exists:
                new_itemList.append(tmpUrl)

        meta = {
                'timeout':10,
                'noImage':True,
                'spider_id':spider_id,
                'bid':bid,
                'gid':gid
                }
        if bookRule['is_js_render'] == True:
            meta['PhantomJs'] = True
        if len(new_itemList) > 0:
            for tmp_url in new_itemList:
                url = format_url(bookRule['base_url'], tmp_url)
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_chapter)
                #  break
            #  update_max_page(spider_id, response.meta['max_page'])
        
    def parse_chapter(self, response):
        bid = response.meta['bid']
        gid = response.meta['gid']
        spider_id = response.meta['spider_id']
        s_group = self.spiderGroup[gid]
        bookRule = json.loads(s_group['rule'])['book']
        volumeRule = json.loads(s_group['rule'])['volume']
        chapterRule = json.loads(s_group['rule'])['chapter']
        if s_group['filter'].strip():
            chapterFilter = json.loads(s_group['filter'])['chapter']
        else:
            chapterFilter = {}
        item = BaseItemParse.parse_chapter_item(response, chapterRule, chapterFilter)
        yield item

    def start_requests2(self):
        #  data = getSpiderList()
        #  data = getRuleList()
        #  print data
        #  img = 'https://pic2.zhimg.com/95b6eff9c4058e26da3a384e51b1c229_xl2.jpg'
        #  ss = saveImage(img)
        #  print ss
        url = 'http://123.56.136.204:9080/?time=2'
        #  url = 'http://www.baidu.com'
        #  url = 'http://www.cailianpress.com'
        #  url = 'http://news.163.com/latest/'
        meta = {
                'PhantomJs':True,
                'noImage':True,
                'timeout':5
                }
        yield scrapy.Request(url=url, meta=meta, callback=self.parse_my)
