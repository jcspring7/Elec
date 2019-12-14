# -*- coding: utf-8 -*-
import sys

#sys.setdefaultencoding('utf-8')

import re
from ..items import newsItem
import scrapy
from scrapy.selector import Selector
from ..spiders import funcsrc
from datetime import date


# 해당 사이트가 크를링이 가능 한지 확인하기  : 이부분이 안되면 크롤할 수 없다..
class newsCrawl(scrapy.Spider):

    name = "newsCrawl"
    
    start_urls = [
        "http://joongang.joins.com/",
    ]

    def parse(self, response):
        page = response.url.split("/")[-1]        
        filename = 'news-%s.html' % page
        print (filename + "================================")
        with open(filename, 'wb') as f:
            f.write(response.body)
                  
class newsCrawl_text(scrapy.Spider):
    name = "newsCrawl_text"
    global count1    
    count1 = 0
    allowed_domains = ["joongang.joins.com"]
    start_urls = [
        "http://joongang.joins.com/"     
    ]   

    print ("start project")
    
    def parse(self, response):    
        
        
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
     
 