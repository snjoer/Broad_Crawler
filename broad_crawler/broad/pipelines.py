# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
import hashlib
import scrapy
from scrapy.http import Request
from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

reload(sys)
sys.setdefaultencoding('utf-8')

class BroadPipeline(object):
    
    def process_item(self, item, spider):
        fname = ''.join(item['title'].split())
        command = 'mkdir ' + fname
        os.system(command) 
        path = fname + '/' + fname
        with open(path, 'w') as f:
            f.write('title: ' + item['title'] + '\n')
            f.write('url: ' + item['url'] + '\n')
            f.write('date: ' + str(item['date']) + '\n')
            f.write('content: ' + item['content'] + '\n')
        return item

class BroadImagesPipeline(ImagesPipeline):
    
    dirname = ""

    def get_media_requests(self, item, info):
        self.dirname = ''.join(item['title'].split())
        return [Request(x) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        filename = self.dirname + '/pic/%s.jpg' % (image_guid)
        return filename
