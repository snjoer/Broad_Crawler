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
        if not os.path.exists(item['title']):
            os.mkdir(item['title']) 
        path = item['title'] + '/' + item['title']
        with open(path, 'w') as f:
            f.write('title: ' + item['title'] + '\n')
            f.write('url: ' + item['url'] + '\n')
            f.write('date: ' + str(item['date']) + '\n')
            f.write('content: ' + item['content'] + '\n')
        return item

class BroadImagesPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        self.dirname = item['title']
        if len(item) > 0:
            return [Request(x) for x in item.get(self.images_urls_field, [])]
 
    def item_completed(self, results, item, info):
        for root, dirs, files in os.walk('full'):
            print len(files)
            if len(files) == 0:
                return item
        if not os.path.exists(item['title']):
            os.mkdir(item['title'])
        os.mkdir(item['title'] + '/pic')
        print "title: " + item['title']
        command = "mv full/* " + item['title'] + '/pic'
        os.system(command)
        return item  
