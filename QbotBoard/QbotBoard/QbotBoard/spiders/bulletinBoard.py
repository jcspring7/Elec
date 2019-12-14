# -*- coding: utf-8 -*- 
'''
Created on 2019. 2. 17.

@author: jcspring

cd G:\source\python\workspace2019\python\QbotBoard\QbotBoard
scrapy crawl "QBot"
scrapy crawl "HelloMobile"
scrapy crawl HelloMobile -o HelloMobile.jl
'''
import scrapy
import json
import os

class QuotesSpider1(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        
class QuotesSpider(scrapy.Spider):
    name = "QBot"


    def start_requests(self):
        return scrapy.FormRequest('http://mobile.cjhello.com/mv_Client/customer/customer03Proc.asp',
                                   formdata={"cate":1, "subCate":1, "page":1, "srhTxt":1, "sortType":1, "pType":"2", "Telecom":"ALL"},
                                   callback=self.parse)     

        

    def parse(self, response):  
        textdata = response.xpath('//a[@href="#a1"]/text()')    #[@class="q"]
        
        jsonresponse = json.loads(response.body.decode("utf-8"))
        print(jsonresponse["meta_description"])
        #datanum = response.xpath('//span[@class="og2 b"]/text()')
        #print (datanum.extract())
        #print("==================================")
        print("==================================",response.body)
        writedata=[]

        for datalist in textdata:
            datadata = datalist.xpath('//a')
            writedata.append("".join(datadata.extract()))       
            print(datadata.extract())
            
            
            
class HelloMobileSpider(scrapy.Spider):
    name = "HelloMobile"

    def start_requests(self):
        category = '헬로모바일'
        kin_urls = 'https://kin.naver.com/search/list.nhn?query=' + category # 
        urls = [kin_urls]
          

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):        
        textdata = response.xpath('//*[@id="s_content"]/div/ul/li/dl/dt/a/@href')
        #datanum = response.xpath('//span[@class="og2 b"]/text()')
        #print (datanum.extract())
        alist = textdata.extract()      
        
        next_link= response.xpath('//*[@class="s_paging"]/a/@href').extract()
        print("next_link", len(next_link)) 
        print("==================================",alist[0])
        for item in alist:
            yield response.follow(item, self.parse_doc)
            
        # 다음 페이지를 자동으로 넘어간다. 중복된 페이지는 scrapy가 url을 체크해서 알아서 처리해줌.
        for next_page in next_link:
            yield response.follow(next_page, self.parse)    
        
         
                    
        # 각 질문의 링크에 들어가서 질문의 본문을 각각 txt 파일로 저장한다.
    def parse_doc(self, response):
        #docId = response.request.url.split("docId=")[-1]
        #title = response.css('span.title_text ::text').extract_first().strip().encode('utf8')
        quest_title = response.xpath('//*[@id="content"]/div[1]/div/div[1]/div[2]/div/div/text()').extract()        
        quest_contents = response.xpath('//*[@id="content"]/div[1]/div/div[1]/div[3]/p/text()').extract()
        question_title = (" ".join(quest_title)).strip()
        question_contents = (" ".join(quest_contents)).strip()
        print("question_title ",question_title," length : ", len(quest_title) )
        print("question_contents ",question_contents," length : ", len(quest_contents) )
        filename = 'kms.txt' 
        with open(filename, "a",  encoding='utf-8') as f:
            f.write(question_title+"#####"+question_contents+"#####"+response.request.url+"@@@@@")        
        
        
        """
        question = "\n\n".encode('utf8')
        for q in question_contents:
            question += q.strip().encode('utf8')
            question += "\n".encode('utf8')
            
        filename = 'raw/%s.txt' % docId
        with open(filename, 'wb') as f:
            f.write(title)        
        """    
"search : 지식인 scrapy "            
class exampleSpider(scrapy.Spider):
    name = 'kinspider' # scrapy의 spider를 실행하기 위해 필요한 매개변수
    category = '5' # 크롤링하고자 하는 카테고리
    kin_urls = 'http://kin.naver.com/qna/list.nhn?dirId=' + category # 네이버 지식인 기본 URL
    start_urls = [kin_urls]

    # 최신 1000개의 질문 목록을 가져온다.
    def parse(self, response):
        # 현재 목록에 각 질문의 링크를 타고 들어간다. parse_doc에서 나머지를 처리함.
        for item in response.css('td.title a'):
            yield response.follow(item, self.parse_doc)

        # 다음 페이지를 자동으로 넘어간다. 중복된 페이지는 scrapy가 url을 체크해서 알아서 처리해줌.
        for next_page in response.css('div.paginate > a'):
            yield response.follow(next_page, self.parse)

    # 각 질문의 링크에 들어가서 질문의 본문을 각각 txt 파일로 저장한다.
    def parse_doc(self, response):
        docId = response.request.url.split("docId=")[-1]
        title = response.css('span.title_text ::text').extract_first().strip().encode('utf8')
        question_contents = response.css('div#contents_layer_0 div._endContentsText ::text').extract()
        question = "\n\n".encode('utf8')
        for q in question_contents:
            question += q.strip().encode('utf8')
            question += "\n".encode('utf8')
            
        filename = 'raw/%s.txt' % docId
        with open(filename, 'wb') as f:
            f.write(title)