# -*- coding: utf-8 -*-
import sys

"""
2017.9.23 python 3.5 로 upgrade함 
중앙일보 연합신문의 그날 데이타를 읽어서 mysql db 에 저장...
"""

#sys.setdefaultencoding('utf-8')

import re
from tutoral2017.items import newsItem
import scrapy
from scrapy.selector import Selector
from tutoral2017.spiders import funcsrc
from datetime import date
# django에 서 읽어갈 수 있는 데이타 크롤
class newsCrawl_text(scrapy.Spider):
    name = "two"   #newsCrawl_multi"
    global count1    
    count1 = 0
    
    print ("start project")
    
    def start_requests(self):
        yield scrapy.Request('http://joongang.joins.com/', self.parsejoong)
        yield scrapy.Request('http://www.yonhapnews.co.kr/', self.parseyonhap)
        
    def parsejoong(self, response):            
        #print 'http://joongang.joins.com/'
        hxs = Selector(response)    
        selects = hxs.xpath('//strong[@class="headline mg"]/a/@href')
        
        #selects = hxs.xpath('//a[contains(@href,"http://news.joins.com/article/")]/@href')
        for sel in selects:
            link = sel.extract()
            #count1 +=1
            #print "---COUNT : ","  ----"   ,link, len(link)
            yield scrapy.Request(link,callback=self.parse_dir_contents,dont_filter=True)   #dont_filter=True   중요
           

            
    def parse_dir_contents(self,response):
        #print "---COUNT : ", count1, "  ----"   ,response.url           
        self.logger.info("Visited %s", response.url)
        
        
        item = newsItem()        
        item['title'] = response.xpath('//div[@class="subject"]/h1/text()').extract_first()         #subject
        
        if item['title'] == None: 
            
            return  #item1['title'] ="" 
        
        item['link'] = response.url
        
        item['srcname'] = funcsrc.srcname(response.url)
        curdate = date.today()       
        item['date'] = str(curdate.year)+"/"+str(curdate.month)+"/"+str(curdate.day)

        rexbefore = " ".join(response.xpath('//div[@id="article_body"]/text()').extract())        
        rexbefore = re.sub("\r|\n|\t","",rexbefore)                
        #item['body'] = rexbefore
             
        #print "++++++", item1['title']
        
        return item    
     
    def parseyonhap(self, response):      
        #print "http://www.yonhapnews.co.kr/"      
        hxs = Selector(response)    
        selects = hxs.xpath('//a[contains(@href, "HTTP://www.yonhapnews.co.kr/")]/@href')
        
        #selects = hxs.xpath('//a[contains(@href,"http://news.joins.com/article/")]/@href')
        for sel in selects:
            link = sel.extract()
            #print link
            yield scrapy.Request(link,callback=self.parse_dir_yonhap,dont_filter=False)   #dont_filter=True   중요
    
    
    
    def parse_dir_yonhap(self,response):   
        #print "http://www.yonhapnews.co.kr/=============="
        self.logger.info("Visited %s", response.url)
        
        
        item = newsItem()        
        item['title'] = response.xpath('//h1[@class="tit-article"]/text()').extract_first()         #subject
        
        if item['title'] == None: 
            
            return  #item1['title'] ="" 
        
        item['link'] = response.url
        
        item['srcname'] = funcsrc.srcname(response.url)
        curdate = date.today()       
        item['date'] = str(curdate.year)+"/"+str(curdate.month)+"/"+str(curdate.day)

        rexbefore = " ".join(response.xpath('//div[@id="article"]/p/text()').extract())        
        rexbefore = re.sub("\r|\n|\t","",rexbefore)                
        #item['body'] = rexbefore   # body만 임시로 막음
             
        #print "++++++", item1['title']
        
        return item    