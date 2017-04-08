#!/usr/bin/env python
# -*- encoding:utf-8 -*-

'''
Database: Broad_Crawler
Table: broad

Table Structure:
CREATE TABLE broad 
(Title varchar(300) NOT NULL, 
Url varchar(300) NOT NULL, 
Date varchar(50) NOT NULL, 
Content TEXT NOT NULL, 
Image_Url TEXT NOT NULL)CHARSET=utf8mb4;
'''

import json
import redis
import pymysql.cursors

def connectRedis():
    conn = redis.StrictRedis(host='localhost', port=6379)
    return conn

def connectMySQL():
    conn = pymysql.connect(host='localhost',
                             user='root',
                             db='broad_crawler',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return conn

def main():
    redis_conn = connectRedis()
    mysql_conn = connectMySQL()
    while True:
        source, data = redis_conn.blpop(['broad:items'])
        item = json.loads(data)
#        try:
#            with mysql_conn.cursor() as cursor:
        cursor = mysql_conn.cursor()
        sql = 'INSERT INTO broad VALUES \
                ("%s", "%s", "%s", "%s", "%s");' %\
                (item['title'], item['url'],\
                item['date'], item['content'], item['image_urls'])
        cursor.execute(sql)
        mysql_conn.commit()
        print "Insert one"
#        except Exception, e:
#            print e.message

if __name__ == '__main__':
    main()
