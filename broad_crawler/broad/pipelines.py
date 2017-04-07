import os
import sys
import hashlib
import scrapy
import pymysql.cursors
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

class MySQLStorePipeline(object):
    def __init__(self):
	self.conn = pymysql.connect(host='localhost',\
                user='root',\
                db='broad_crawler',\
                charset='utf8',\
                cursorclass=pymysql.cursors.DictCursor)
    def process_item(self, item, spider):
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO broad VALUES \
                        ('%s', '%s', '%s', '%s', '%s')" %\
                        (item['title'], item['url'],\
                        item['date'], item['content'], item['image_urls'])
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            print e.message
        finally:
            self.conn.close()
