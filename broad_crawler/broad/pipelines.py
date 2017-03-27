# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class BroadPipeline(object):
    def process_item(self, item, spider):
        fname = item['title']
        with open(fname, 'w') as f:
            f.write('title: ' + item['title'] + '\n')
            f.write('url: ' + item['url'] + '\n')
            f.write('date: ' + str(item['date']) + '\n')
            f.write('content: ' + item['content'] + '\n')
        return item
