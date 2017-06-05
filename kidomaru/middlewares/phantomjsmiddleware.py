# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.exceptions import *
import time
import signal

class PhantomJsMiddleware(object):

    def process_request(self, request, spider):
        if request.meta.has_key('PhantomJs'):
            print 'PhantomJs is starting...'
            service_args = []
            timeout = 10
            if request.meta.has_key('noImage') and request.meta['noImage'] == True:
                service_args.append('--load-images=false')
            if request.meta.has_key('timeout') and request.meta['timeout'] > 0:
                timeout = request.meta['timeout']
            service_args.append('--disk-cache=true')
            service_args.append('--ignore-ssl-errors=true')
            dr = webdriver.PhantomJS('/home/ching/www/novel_spider/bin/phantomjs', service_args=service_args)
            try:
                dr.set_page_load_timeout(timeout)
                dr.set_script_timeout(timeout)
                dr.get(request.url)
                time.sleep(1)
                html = dr.page_source
                dr.service.process.send_signal(signal.SIGTERM)
                dr.quit()
                return HtmlResponse(request.url, encoding='utf-8', body=html, request=request)
            except Exception as ex:
                dr.service.process.send_signal(signal.SIGTERM)
                dr.quit()
                #return return None 还会被其他middleware 执行，所以raise 出去
                raise IgnoreRequest("Ignore request for PhantomJs timeout: %s" % request.url)
        else:
            return

