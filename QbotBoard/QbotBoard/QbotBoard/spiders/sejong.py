# -*- coding: utf-8 -*- 
'''
Created on 2019. 4. 10.

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
import re
#from ..items import HelloItem
#from QbotBoard.QbotBoard.items import HelloItem

# 파라미터를 전달하는 방법
#http://doc.scrapy.org/en/latest/topics/request-response.html#passing-additional-data-to-callback-functions

# 2019.4.10 세종대학교 자주하는 질문 --
# 학사 : http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=697
# 장학 : http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=698
# 등록 : http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=698
# 국제교류 : http://board.sejong.ac.kr/pages/faq.html
# 학술정보원 : http://library.sejong.ac.kr/bbs/Bbs.ax?bbsID=3
# 전산 : http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=353

class SejongSpider(scrapy.Spider):
    name = "Sejong"
    
    category = ["로밍"]
    def start_requests(self):
        
        for cate in self.category:           
            url = 'http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=698'
            request = scrapy.Request(url=url, callback=self.parse, encoding='utf-8')
            #request.meta['cate'] = cate 
            yield  request                        

    """
http://board.sejong.ac.kr/boardlist.do
 name="currentPage" 
 name="bbsConfigFK" value="697"
 name="searchField" value="ALL"
 name="searchValue" value=""
 name="searchLowItem" value="ALL"
    """
    def parse(self, response):        
        title = response.xpath('/html/body/div/table/tbody/tr/td[2]/a/@href').extract()
        next_link= response.xpath('//a[@class="no"]/text()').extract()                                   
        
        print("next link : ", " ".join(next_link), "-------------")
        
        #cate = response.meta['cate']
        
       
        for item in title:
            print("item")
            
            respon = response.follow(item, self.parse_doc, encoding='utf-8',  )
            #respon.meta["cate"] = cate
            yield respon
    
        # 다음 페이지를 자동으로 넘어간다. 중복된 페이지는 scrapy가 url을 체크해서 알아서 처리해줌.
        for next_page in next_link:
            
            """
            yield scrapy.FormRequest(url="http://board.sejong.ac.kr/boardlist.do",
                    formdata={'currentPage': '1', 'bbsConfigFK': '697',
                              'searchField': 'ALL', 
                              "searchValue" :"" ,"searchLowItem" :"ALL"},
                             callback=self.parse)
            """                 
  #http://board.sejong.ac.kr/boardlist.do?currentPage=2&bbsConfigFK=697&searchField=ALL&searchValue=%27%27&searchLowItem=ALL          
            next_url= "http://board.sejong.ac.kr/boardlist.do?currentPage="+ next_page +"&bbsConfigFK=698&searchField=ALL&searchValue=%27%27&searchLowItem=ALL"
            print("next_url : ",next_url)
            
            respon = response.follow(next_url, self.parse, encoding='utf-8', )
            
            yield respon 



        # 각 질문의 링크에 들어가서 질문의 본문을 각각 txt 파일로 저장한다.
    def parse_doc(self, response):     
        quest_title = response.xpath('/html/body/div/table[1]/thead/tr[1]/td/text()').extract()        
        quest_contents = response.xpath('/html/body/div/table[1]/tbody/tr/td/descendant-or-self::*/text()').extract()  #[not(name()="br")]
        quest_date = response.xpath('/html/body/div/table[1]/thead/tr[2]/td[2]/text()').extract()                                      
         
        question_title = (" ".join(quest_title)).strip()                             
        question_contents = " ".join(quest_contents).strip()          # +" ".join(quest_content2).strip()
        
        """
        space_repl = re.compile(r'\n|\s')        
        question_contents = re.sub(r'\n|\s', '', question_contents)
        """                  
        question_contents=""
        for cont in quest_contents:
            print("cont :",cont.strip("\s"),"---")
            question_contents +=  cont.replace("\n","").strip()    #.replace("&nbsp","")
 
                  
        question_contents = question_contents.replace(r'\n',"")         
        question_date = " ".join(quest_date).strip()
        
#        print("question_title ",question_title," length : ", len(quest_title) )
    
        #cate = response.meta['cate']
        filename = 'sejong.txt' 
        with open(filename, "a",  encoding='utf-8') as f:
            f.write(question_title+"\t"+ question_date +"\t"+question_contents+"\t"+response.request.url+ "\n")        
       


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
