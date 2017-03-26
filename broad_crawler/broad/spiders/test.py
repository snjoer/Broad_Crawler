#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

def crawl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    divs = soup.findAll('div')
    div_ps = {}
    for div in divs:
        ps = div.findAll('p')
        div_ps[len(ps)] = div
    div_ps = sorted(div_ps.iteritems(), key=lambda d:d[0], reverse=True)
    ps = div_ps[0][1].findAll('p')
    for p in ps:
        print p.text

if __name__ == '__main__':
    url = 'http://www.guokr.com/article/442057/'
    crawl(url)
