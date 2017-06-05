#!/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
import urllib
import urllib2
import HTMLParser
import logging
import time
import signal
import sys 
reload(sys)
sys.setdefaultencoding( "utf-8" )

def call_phantomjs_service(url):
    re_content = ''
    api = 'http://10.170.254.117:6666/?url='
    url = api + urllib.unquote(url)
    try:
        req = urllib2.Request(url)
        res = urllib2.urlopen(req, timeout=15)
        re_content = res.read()
    except Exception as ex:
        logging.warning("recieve data from phantomjsService failed: %s url: %s"%(ex, url))
    return re_content

def call_phantomjs(url, optional = None):
    re_content=""
    service_args = []
    timeout = 10
    if optional is not None:
        if optional.has_key('noImage') and optional['noImage'] == True:
            service_args.append('--load-images=false')
        if optional.has_key('timeout') and optional['timeout'] > 0:
            timeout = optional['timeout']

    service_args.append('--disk-cache=true')
    service_args.append('--ignore-ssl-errors=true')
    dr = webdriver.PhantomJS('/home/ching/www/novel_spider/bin/phantomjs', service_args=service_args)
    try:
        #  dr.implicitly_wait(3)
        dr.set_page_load_timeout(timeout)
        dr.set_script_timeout(timeout)
        dr.get(url)
        time.sleep(1)
        #  html_parser = HTMLParser.HTMLParser()
        sou = dr.page_source
        re_content = sou
        #  re_content = html_parser.unescape(sou)
    except Exception as ex:
        logging.warning(" PhantomJS url:%s failed:%s" % (url, ex))
        dr.service.process.send_signal(signal.SIGTERM)
        dr.quit()
    dr.service.process.send_signal(signal.SIGTERM)
    dr.quit()
    return re_content

def generate_image(url, image_path):
    dr = webdriver.PhantomJS('./bin/phantomjs')
    dr.set_window_size(1366,768)
    dr.get(url)
    js = """
var itv = setInterval(function(){
    var prevScrollHeight = document.body.scrollTop;
    window.scrollTo(0, document.body.scrollTop + 100);
    if(prevScrollHeight == document.body.scrollTop){
        clearInterval(itv);
    }
}, 10);
    """
    #  dr.execute_script(js)
    dr.save_screenshot(image_path)
    dr.quit()

