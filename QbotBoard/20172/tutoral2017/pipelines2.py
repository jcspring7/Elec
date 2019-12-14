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
import MySQLdb.cursors
import sys


class Tutoral2017Pipeline(object):
    def __init__(self):
        self.file = codecs.open(settings['FILENAME'], 'w', encoding='utf-8')
    
        try:
            self.conn = MySQLdb.connect(user=settings['MYSQLDB_USERNAME'], 
                                        passwd=settings['MYSQLODB_PASSWORD'], 
                                        db=settings['MYSQLDB_DATABASE'], 
                                        host=settings['MYSQLDB_HOST'], 
                                        charset="utf8", use_unicode=True)
            print("1. db Connect success")
            self.cursor = self.conn.cursor()
            print("2")
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)                 
        #log data to json file
    
    def process_item(self, item, spider): 
        print "pipeline"    
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
        except MySQLdb.Error, e:
            print "Errorspring %d: %s" % (e.args[0], e.args[1])
            return item  
        
    def spider_closed(self,spider):
        self.file.close()
        
        
        
        #print item['desc'],"==========================="            
        #self.cursor.execute("insert into newspaper.news(title, body, num) values ( %s, %s, %s)", (item['title'].encode('utf-8'), item['desc'].encode('utf-8'),item['num'].encode('utf-8')))
        