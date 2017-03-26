# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BroadPipeline(object):
    def process_item(self, item, spider):
        title = '/Users/rafaelcheng/broad_spider/broad/' + item['title']
        with open(title, 'w') as f:
            f.write(title)
            f.write(item['url'])
            f.write(item['date'])
            f.write(item['content'])
        return item
