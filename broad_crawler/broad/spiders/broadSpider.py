#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import re
import sys 
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from broad.items import BroadItem 
   
reload(sys)
sys.setdefaultencoding('utf-8')
   
class broadSpider(scrapy.Spider):
    name = "broad"
   
    start_urls = ["http://www.guokr.com"]
      
    def parse(self, response):
        items = self.parse_page(response)
        if items['title'] != '': 
            yield items
        requests = self.extract_links(response)
        for request in requests:
            yield request
   
    def extract_links(self, response):
        r = []
        link_extractor = LinkExtractor()
        if isinstance(response, HtmlResponse):
            links = link_extractor.extract_links(response)
            r.extend(Request(x.url, callback=self.parse) for x in links)
        return r
       
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
            item['image_urls'] = []
            for img in images:
                if 'http' in img['src']:
                    item['image_urls'].append(img['src'])
            text = ""
            for p in ps:
                text += p.text
            item['content'] = text
        return item         
