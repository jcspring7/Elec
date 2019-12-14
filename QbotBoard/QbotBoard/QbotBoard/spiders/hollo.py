# -*- coding: utf-8 -*- 
'''
Created on 2019. 2. 17.

@author: jcspring

cd G:\source\python\workspace2019\python\QbotBoard\QbotBoard
scrapy crawl "QBot"
scrapy crawl "HelloMobile"
scrapy crawl HelloMobile -o HelloMobile.jl

#arg 사용하는 방법
scrapy crawl quotes -o quotes-humor.json -a tag=humor
 tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag

'''
import scrapy
import json
import os
from ..items import HelloItem
#from QbotBoard.QbotBoard.items import HelloItem

# 파라미터를 전달하는 방법
#http://doc.scrapy.org/en/latest/topics/request-response.html#passing-additional-data-to-callback-functions

class HelloMobileSpider(scrapy.Spider):
    name = "Hello"
    category = ["명의변경","개통"]
    
    def start_requests(self):
        """
        urls = ['https://kin.naver.com/search/list.nhn?query=' + "헬로모바일" +"+" + self.category[0],
                'https://kin.naver.com/search/list.nhn?query=' + "헬로모바일" +"+" + self.category[1],
                ]
        """  
        
        for cate in self.category:           
            url = 'https://kin.naver.com/search/list.nhn?query=' + "헬로모바일" + "+" + cate   
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['cate'] = cate 
            yield  request
            #yield scrapy.Request(url=url, callback=self.parse)
            


    def parse(self, response):        
        textdata = response.xpath('//*[@id="s_content"]/div/ul/li/dl/dt/a/@href')
        alist = textdata.extract()      
        
        next_link= response.xpath('//*[@class="s_paging"]/a/@href').extract() 
        
        cate = response.meta['cate']

        for item in alist:
            respon = response.follow(item, self.parse_doc)
            respon.meta["cate"] = cate
            yield respon
    
        # 다음 페이지를 자동으로 넘어간다. 중복된 페이지는 scrapy가 url을 체크해서 알아서 처리해줌.
        for next_page in next_link:
            respon = response.follow(next_page, self.parse)
            respon.meta["cate"] = cate   
            yield respon             
                    

        # 각 질문의 링크에 들어가서 질문의 본문을 각각 txt 파일로 저장한다.
    def parse_doc(self, response):     
        quest_title = response.xpath('//*[@id="content"]/div[1]/div/div[1]/div[2]/div/div/text()').extract()        
        quest_contents = response.xpath('//*[@id="content"]/div[1]/div/div[1]/div[3]/descendant-or-self::*/text()').extract()
        question_title = (" ".join(quest_title)).strip()
        question_contents = (" ".join(quest_contents)).strip()
        print("question_title ",question_title," length : ", len(quest_title) )
        if len(quest_contents) > 0 :
            print("question_contents ",question_contents," length : ", len(quest_contents) )
        
        cate = response.meta['cate']

        #filename = 'crawdata/kms_'+ cate  +'.txt'
        filename = 'crawdata/kms.txt' 
        with open(filename, "a",  encoding='utf-8') as f:
            f.write(cate +"\t"+question_title+"\t"+question_contents+"\t"+ response.url+"\n")
            
                    

class HelloDBSpider(scrapy.Spider):
    name = "HelloDB"
    category = ["명의변경"]  #,"개통"
    
    def start_requests(self):
        
        for cate in self.category:           
            url = 'https://kin.naver.com/search/list.nhn?query=' + "헬로모바일" + "+" + cate   
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['cate'] = cate 
            yield  request
            #yield scrapy.Request(url=url, callback=self.parse)
            


    def parse(self, response):        
        textdata = response.xpath('//*[@id="s_content"]/div/ul/li/dl/dt/a/@href')
        alist = textdata.extract()      
        
        next_link= response.xpath('//*[@class="s_paging"]/a/@href').extract() 
        
        cate = response.meta['cate']

        for item in alist:
            respon = response.follow(item, self.parse_doc)
            respon.meta["cate"] = cate
            yield respon
    
        # 다음 페이지를 자동으로 넘어간다. 중복된 페이지는 scrapy가 url을 체크해서 알아서 처리해줌.
        for next_page in next_link:
            respon = response.follow(next_page, self.parse)
            respon.meta["cate"] = cate   
            yield respon             
                    

        # 각 질문의 링크에 들어가서 질문의 본문을 각각 txt 파일로 저장한다.
    def parse_doc(self, response):     
        quest_title = response.xpath('//*[@id="content"]/div[1]/div/div[1]/div[2]/div/div/text()').extract()        
        quest_contents = response.xpath('//*[@id="content"]/div[1]/div/div[1]/div[3]/descendant-or-self::*/text()').extract()
        question_title = (" ".join(quest_title)).strip()
        question_contents = (" ".join(quest_contents)).strip()
        print("question_title ",question_title," length : ", len(quest_title) )
        if len(quest_contents) > 0 :
            print("question_contents ",question_contents," length : ", len(quest_contents) )
        
        cate = response.meta['cate']

        #filename = 'crawdata/kms_'+ cate  +'.txt'
        filename = 'crawdata/kms.txt' 
        with open(filename, "a",  encoding='utf-8') as f:
            f.write(cate +"\t"+question_title+"\t"+question_contents+"\t"+ response.url+"\n")        

        HelloItem['cate'] = cate
        HelloItem['Qtitle'] = question_title
        HelloItem['Qtitle_content'] = question_contents
        HelloItem['answer'] = ""
        HelloItem['link_url'] = response.url
        
        return HelloItem


"""
ctrl+alt+down  : 현재행 복사
Ctrl + D : 행 제거
Alt+SHFT+UP(반복) = 현재 커서의 멤버를 선택 CTRL+ PAGEUP/PAGEDOWN = 현재 파트(에디터or 뷰)에서 이전/이후의 ...
Alt+SHFT+UP(반복) = 현재 커서의 멤버를 선택
CTRL+ PAGEUP/PAGEDOWN = 현재 파트(에디터or 뷰)에서 이전/이후의 에디터나 뷰로 이동
ART+SHIFT+M = 선택 된 라인을 METHOD로 생성
CTRL + T = 부모 클래스나 인터페이스에 Qick Type hierarchy를 보여 줌
ART+SHIFT+A = 에디터에서 커서가 vertical로 선택 할수 있게 바뀜. 한 번더 누르면 커서가 원 상태로 복귀
CTRL+W = 현재 에디터 닫기
"""
        