#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import re
import sys 
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from broad.items import BroadItem 
   
reload(sys)
sys.setdefaultencoding('utf-8')
   
class broadSpider(RedisSpider):
    name = "broad"
   
    redis_key = 'link'

    def parse(self, response):
        items = self.parse_page(response)
        if items['title'] != '': 
            yield items
        requests = self.extract_links(response)
   
    def extract_links(self, response):
        link_extractor = LinkExtractor()
        if isinstance(response, HtmlResponse):
            links = link_extractor.extract_links(response)
            for link in links:
                os.system('redis-cli lpush link ' + link)

    def parse_page(self, response):
        item = BroadItem()
        soup = BeautifulSoup(response.text, "lxml")
        title = response.xpath('//title/text()').extract()
        if len(title) > 0:
            item['title'] = ''.join(title[0].replace('|', ',').\
                    replace('\"', '').replace('\'', '').\
                    replace('(', '[').replace(')', ']').\
                    replace('#', '').split())
        else:
            item['title'] = ''
        print item['title']
        item['url'] = response.url
        try: 
            time = response.xpath('//text()').re_first(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')                                                                                   
            item['time'] = time
        except Exception:
            item['date'] = "none"
        divs = soup.findAll('div')
        div_dic = {}
        for div in divs:
            ps = div.findAll('p')
            div_dic[len(ps)] = div
        if len(div_dic) == 0:
            item['content'] = "none"
        else:
            div_dic = sorted(div_dic.iteritems(), key=lambda d:d[0], reverse=True)
            ps = div_dic[0][1].findAll('p')
            images = div_dic[0][1].findAll('img')
            item['image_urls'] = ''
            for img in images:
                if 'http' in img['src']:
                    item['image_urls'] += img['src'] + '\n'
            text = ""
            for p in ps:
                text += p.text
            item['content'] = text
        return item         
