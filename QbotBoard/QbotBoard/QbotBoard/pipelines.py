# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import cx_Oracle
from scrapy.conf import settings
#from scrapy import log 
#from twisted.enterprise import adbapi
#import MySQLdb.cursors
import pymysql                            #2017. 09.23  MySQLdb python3.x 가 없어서 pymysql로 바꿔서 db 연결설정
import sys


class QbotboardPipeline(object):
    def __init__(self):
        
        self.file = codecs.open(settings['FILENAME'], 'w', encoding='utf-8')
    
        try:
            #conn = cx_Oracle.connect('Username/Password@IP:PORT/SID')
            self.conn = cx_Oracle.connect('DBTEST/dbgood@localhost:1521/orcl',mode=cx_Oracle.SYSDBA)               
            
            #self.conn = pymysql.connect(host="localhost",user="spring",passwd="i4spring!!",db="topicker",charset="utf8", use_unicode=True)                                     
            """    
            self.conn = cx_Oracle.connect(user=settings['ORACLEDB_USERNAME'], 
                                        passwd=settings['ORACLEDB_PASSWORD'], 
                                        db=settings['ORACLEDB_DATABASE'], 
                                        host=settings['ORACLEDB_HOST'], 
                                        charset="utf8", use_unicode=True)
            """                            
            print("1. db Connect success")
            self.cursor = self.conn.cursor()
            print("2")
            
        except cx_Oracle.DatabaseError as e: 
            print ("Error " )
            sys.exit(1) 
            raise Exception("DB Connection Error({0}):".format(e))    
                    
        #log data to json file    
        
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"       
        self.file.write(line)
        
        try:
            self.cursor.execute("insert into QUESTION(QUEST_ID, CATEGORY,QUESTION,\
                                   CONTENT,ANSWER,URL,CREDATE) values ( %d, %s, %s, %s, %s, %s,%d)", \
                                    (1, item['cate'],item['Qtitle'],item['Qtitle_content'],item['answer'],item['link_url']))
            self.conn.commit()
        except cx_Oracle.DatabaseError:
            print ("Error " )
            return item  
    
            
    def spider_closed(self,spider):
        self.file.close()
