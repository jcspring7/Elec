# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

from scrapy.conf import settings
#from scrapy import log 
#from twisted.enterprise import adbapi
#import MySQLdb.cursors
#import pymysql                            #2017. 09.23  MySQLdb python3.x 가 없어서 pymysql로 바꿔서 db 연결설정
import cx_Oracle
import sys


class Tutoral2017Pipeline(object):
    def __init__(self):
        self.file = codecs.open(settings['FILENAME'], 'w', encoding='utf-8')
    
        try:
            self.conn = pymysql.connect(user=settings['ORACLEDB_USERNAME'], 
                                        passwd=settings['ORACLEDB_PASSWORD'], 
                                        db=settings['ORACLEDB_DATABASE'], 
                                        host=settings['ORACLEDB_HOST'], 
                                        charset="utf8", use_unicode=True)
            print("1. db Connect success")
            self.cursor = self.conn.cursor()
            print("2")
        except pymysql.err.DatabaseError:
            print ("Error " )
            sys.exit(1)                 
        #log data to json file
    
    def process_item(self, item, spider): 
        print ("pipeline" )   
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"       
        self.file.write(line)
        #self.file.write(item['title'] + "\n")  
        #self.file.write("==============================================")
        
        try:
            #body is null
            #self.cursor.execute("insert into newspaper.newsbody(title, body, link, srcname, date) values ( %s, %s, %s, %s, %s)", (item['title'], item['body'],item['link'],item['srcname'],item['date']))
            
            #2017.7.25 
            #self.cursor.execute("insert into newspaper.newsbody(title, body, link, srcname, date) values ( %s, %s, %s, %s, %s)", (item['title'], "",item['link'],item['srcname'],item['date']))
            self.cursor.execute("insert into newsdb.polls_newsbody(title, link, srcname, date) values ( %s, %s, %s, %s)", (item['title'], item['link'],item['srcname'],item['date']))
            self.conn.commit()
        except pymysql.err.DatabaseError:
            print ("Error " )
            return item  
        
    def spider_closed(self,spider):
        self.file.close()
        
        
        
        #print item['desc'],"==========================="            
        #self.cursor.execute("insert into newspaper.news(title, body, num) values ( %s, %s, %s)", (item['title'].encode('utf-8'), item['desc'].encode('utf-8'),item['num'].encode('utf-8')))
        