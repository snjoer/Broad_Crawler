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

#--------------------------------------------------below
def isTime(d):
    strLen = len(d)
    digit_count = 0
    for dd in d:
        if dd.isdigit():
            digit_count += 1
    if 30 > strLen > 5 and digit_count*1.0 / strLen > 0.5 and digit_count > 8:
        return 1
    else:
        return 0

def pre_process(times):
    times = [tm.replace('\n', '').replace('\t', '').replace('\b', '').replace('&nbsp;', '') for tm in times]
    times = [tm for tm in times if 100 > len(tm) > 0]
    return times


def h1index(title, times):
    find_hi_index = 1
    index = len(times) - 1
    times = times[::-1]
    i = 0
    while i < index and find_hi_index:
        try:
            a = times[i][0]
        except IndexError:
            print 'ERROR index', i
        else:
            b = title
        if a in b:
            find_hi_index -= 1
        i += 1
    return i

#--------------------------------------------------above
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
        #--------------------------------------------------below
        data = response.body
        try:
            chatset = response.encoding
            data = data.decode(chatset, errors='ignore')
        except UnicodeDecodeError as e:
            print e
            raise UnicodeDecodeError
        else:
            title = response.css('title::text').extract_first()
            title = title.replace('\n', '')
            times = re.findall(r'>\s*([\s\S]*?)\s*<', data)
            times = pre_process(times)
            start_i = 0
            # start_i = h1index(title,times)
            for i in range(start_i, len(times)):
                tm = times[i]
                if isTime(tm):
                    item['date'] = tm
                    break
            else:item['date'] = "none"

        #try: 
        #    time = response.xpath('//text()').re_first(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')                                                                                   
        #    item['date'] = time
        #except Exception:
        #    item['date'] = "none"
        #--------------------------------------------------above
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
