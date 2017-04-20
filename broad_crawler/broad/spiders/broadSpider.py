#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os
import re
import sys 
import time
import scrapy
from bs4 import BeautifulSoup
from broad.items import BroadItem
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
from obtain_date import obtain_d
reload(sys)
sys.setdefaultencoding('utf-8')


class BroadCrawlSpider(RedisSpider):
    name = "broad"
    redis_key = "start_url"
    postfix = ""

    def __init__(self):
        settings = get_project_settings()
        self.__class__.postfix = settings.get('POSTFIX')

    def parse(self, response):
        links = self.extractLinks(response)
        items = self.parse_page(response)
        if items['title'] != '':
            yield items
        links = self.extractLinks(response)
        for link in links:
            yield scrapy.Request(link, callback=self.parse)

    def extractLinks(self, response):
        retv = []
        link_extractor = LinkExtractor()
        if isinstance(response, HtmlResponse):
            links = link_extractor.extract_links(response)
            for link in links:
                if self.postfix in link.url:
                    retv.append(link.url)
        return retv
    
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
        print response.url
        item['url'] = response.url

        item['date'] = obtain_d(response)
        print item['date']

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
                try:
                    if 'http' in img['src']:
                        item['image_urls'] += img['src'] + '\n'
                except Exception as e:
                    pass
            text = ""
            for p in ps:
                text += p.text
            item['content'] = text.replace('"', '\'\'')
        return item         
