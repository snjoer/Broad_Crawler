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
import sqlite3
from scrapy.utils.project import get_project_settings

connR = 1
connM = 0
connS = 1


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


def connectSQLite():
    # settings = get_project_settings()
    # sqlite_name = settings.get('sqlite_name')
    # conn = sqlite3.connect(str(sqlite_name))
    conn = sqlite3.connect('sample.db')
    return conn


def to_SQLite(sqlite_conn, item):
    try:
        c = sqlite_conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS broad 
        (Title varchar(300) NOT NULL, 
        Url varchar(300) NOT NULL, 
        Date varchar(50) NOT NULL, 
        Content TEXT NOT NULL, 
        Image_Url TEXT NOT NULL)""")
        record = (item['title'], item['url'], \
                  item['date'], item['content'], item['image_urls'])

        c.execute('INSERT INTO broad VALUES (?,?,?,?,?)', record)
        sqlite_conn.commit()
        print "Insert one"
    except Exception as e:
        print e.message
        with open('failed', 'a') as f:
            f.write(item['url'] + '\n')

def to_MySQL(mysql_conn ,item):
    try:
        with mysql_conn.cursor() as cursor:
            cursor = mysql_conn.cursor()
            sql = 'INSERT INTO broad VALUES \
                    ("%s", "%s", "%s", "%s", "%s");' % \
                  (item['title'], item['url'], \
                   item['date'], item['content'], item['image_urls'])
            cursor.execute(sql)
            mysql_conn.commit()
        print "Insert one"
    except Exception, e:
        print e.message
        with open('failed', 'a') as f:
            f.write(item['url'] + '\n')

def main():
    if connR: redis_conn = connectRedis()
    if connM: mysql_conn = connectMySQL()
    if connS: sqlite_conn = connectMySQL()
    while True:
        source, data = redis_conn.blpop(['content:items'])
        item = json.loads(data)
        if connM: to_MySQL(mysql_conn, item)
        if connS: to_MySQL(sqlite_conn, item)

if __name__ == '__main__':
    main()
