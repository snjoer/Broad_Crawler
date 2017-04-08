#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import re
import sys 
import time
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from broad.items import BroadItem 
   
reload(sys)
sys.setdefaultencoding('utf-8')

class linkExtractorSpider(RedisSpider):
    name = "link"
    redis_key = 'link'

    def parse(self, response):
        link_extractor = LinkExtractor()
        if isinstance(response, HtmlResponse):
            links = link_extractor.extract_links(response)
            for link in links:
                os.system('redis-cli lpush page ' + link.url)
        time.sleep(30)
