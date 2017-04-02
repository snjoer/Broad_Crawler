#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import re
import sys
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from broad.items import BroadItem
import logging
# reload(sys)
# sys.setdefaultencoding('utf-8')

def isTime(d):
    strLen = len(d)
    digit_count = 0
    for dd in d:
        if dd.isdigit():
            digit_count += 1
    if 30 > strLen > 5 and digit_count / strLen > 0.5 and digit_count > 8:
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
            logging.warning('ERROR index {0}'.format(i))
        else:
            b = title
        if a in b:
            find_hi_index -= 1
        i += 1
    return i



class broadSpider(scrapy.Spider):
    name = "broad"

    allowed_domains = ['news.sina.com.cn']
    start_urls = ["http://news.sina.com.cn/"]
    rules = (
        Rule(LinkExtractor(allow=r'news.sina.com.cn'), callback='parse', follow=True),
    )
    
    def parse(self, response):
        self.parse_page(response)
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
#        item = BroadItem()
        soup = BeautifulSoup(response.text, "lxml")
#        item['title'] = response.xpath('//head/title/text()').extract()[0]
#        item['url'] = response.url
        print(response.xpath('//head/title/text()').extract()[0])
        print(response.url)



        # begin TIME-------------------------- 170402


        data = response.body
        try:
            chatset = response.encoding
            data = data.decode(chatset, errors='ignore')
        except UnicodeDecodeError as e:
            print(e)
        else:
            title = response.css('title::text').extract_first()
            title = title.replace('\n', '')
            times = re.findall(r'>\s*?(.*?)\s*?<', data)
            times = pre_process(times)
            start_i = h1index(title,times)
            start_i = 0
            # print(times)
            for i in range(start_i, len(times)):
                tm = times[i]
                if isTime(tm):
                    time = tm
                    # item['time'] = time
                    print('DATE:', time)
                    break
            else:
                # item['date'] = None
                print('DATE:', 'None')

            # end TIME--------------------------


        divs = soup.findAll('div')
        div_dic = {}
        for div in divs:
            ps = div.findAll('p')
            div_dic[len(ps)] = div
        if len(div_dic) == 0:
#            item['content'] = None
            print("None")
        else:
            div_dic = sorted(div_dic.items(), key=lambda d:d[0], reverse=True)
            ps = div_dic[0][1].findAll('p')
            text = ""
            for p in ps:
                text += p.text
#            item['content'] = text
            print(text)
#        yield item
