# -*- coding:utf-8 -*-

'''
Created on 2018. 2. 5
@author: spring
'''

import scrapy
import codecs
import re

class BibleSpider(scrapy.Spider):
    name = "bible"

    def start_requests(self):
        urls = [            
            #'http://bible.c3tv.com/bible/read/read.asp?MenuCd=2',
            'http://bible.c3tv.com/bible/read/read_cont_div.asp?KindBCdArr=;3&CtgACd=1&CtgBCd=19&Jang=72&MenuCd=2',
        ]
        """
        Params='KindBCdArr='+SearchForm.KindBCdArr.value+'&
                  CtgACd='+rdo_CtgACd+'&
                  CtgBCd='+document.getElementById("CtgBCd").value+'&
                  Jang='+document.getElementById("Jang").value+'&
                  MenuCd=2';
        """          
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


        

    def parse(self, response):  
        textdata = response.xpath('//td[@class="p13 kor ln16"]')
        #datanum = response.xpath('//span[@class="og2 b"]/text()')
        #print (datanum.extract())
        #print("==================================")
        print("==================================",response.request)
        writedata=[]

        for datalist in textdata:
            datadata = datalist.xpath('*/text()|text()')
            writedata.append("".join(datadata.extract()))           

        """
        filename = 'test1.html'
        print(writedata)    
        with open(filename, 'w', encoding='utf-8', newline='\n') as f:
            newlinedata = re.sub('</td>','</td>\n',str(writedata))
            f.write(str(newlinedata))
        self.log('Saved file %s' % filename)
        """
#성서 사이트 읽어오기        : 성서 하나만 읽을 수 있다
class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        return [scrapy.FormRequest("http://bible.c3tv.com/bible/read/read_cont_div.asp",
                                   formdata={'KindBCdArr': ';3', 'CtgACd': '1'
                                             , 'CtgBCd': '22', 'Jang': str(k), 'MenuCd': '2'},
                                   callback=self.logged_in) for k in range(1,9)]
        
        
    """
    'CtgBCd': '19' => 시편  Jang = 150장
    'CtgBCd': '20' => 잠언  Jang = 31장
    'CtgBCd': '21' => 전도서  Jang = 12장
    'CtgBCd': '22' => 아가  Jang = 8장
    """
        
               
    def logged_in(self, response):
        textdata = response.xpath('//td[@class="p13 kor ln16"]')
        #para= response.parameters()       
        print('response.request.body : ',response.request.body)
        with open("bible.txt", "a",  encoding='utf-8') as f:
            f.write(str('0') + str(response.request)+str(response.request.body)+'\n')
            f.write(str('0') + str(response.request.body)+'\n')
            
        parm=str(response.request.body,'utf-8')
        jangs = re.findall(r'Jang=\d{1,3}',parm)[0]
        jang = re.sub('Jang=','',jangs)

        writedata=[]

        for datalist in textdata:
            datadata = datalist.xpath('*/text()|text()')
            writedata.append("".join(datadata.extract()))    
            print("".join(datadata.extract()))       
  
        with open("bible.txt", "w",  encoding='utf-8') as f:  #1,3,5,7....:문장  0,2,4,6....:번호            #print(str(writedata))
            i=1
            for k in range(0,len(writedata),2):
                print(str(i)+'\t'+writedata[k+1])
                f.write(str(jang) + '\t' +str(i)+'\t'+writedata[k+1]+'\n')
                i += 1
                            
"""
2018.3.23 성서사이트 구약 전부 읽어오기
G:\source\python\workspace\bible>scrapy crawl myspider 
4개의 text file로 저장 -> 엑셀로 읽어들여서 저장하면  bayes\bible3\keywordout180330.py
def bible_wordCount_pandas1()함수를 이용해 keyword 정렬
"""                           
class Misnet_Spider(scrapy.Spider):
    name = 'Misnet'

    def start_requests(self):
        each_jang=[0,51,41,28,37,35,25,22,5,32,25,23,26,30,\
                   37,11,14,11,43,151,32,13,9,67,53,6,49,13,\
                   15,4,10,2,5,8,4,4,4,3,15,5] 
        #0번째 값은 읽히지 않는 가짜값, 1번재 51이 창세기의 장수보다 1많은수
        #51,41,28,37,35,25,22,5,32,25,23,26,30,37,11,14,11,43,151,32,13,9,67,53,6,49,13,15,4,10,2,5,8,4,4,4,3,15,5
        return [scrapy.FormRequest("http://bible.c3tv.com/bible/read/read_cont_div.asp",
                                   formdata={'KindBCdArr': ';3', 'CtgACd': '1'
                                             , 'CtgBCd': str(i), 'Jang': str(k), 'MenuCd': '2'},
                                   callback=self.logged_in) for i in range(1,40) for k in range(1,each_jang[i])]
    """
    'CtgBCd': '19' => 시편  Jang = 150장
    'CtgBCd': '20' => 잠언  Jang = 31장
    'CtgBCd': '21' => 전도서  Jang = 12장
    'CtgBCd': '22' => 아가  Jang = 8장
    """
        
               
    def logged_in(self, response):
        with open("bible.txt", "a",  encoding='utf-8') as f:
            f.write(str('0') + str(response.request)+str(response.request.body)+'\n')
                 
        textdata = response.xpath('//td[@class="p13 kor ln16"]')
        #para= response.parameters()
               
        #print(response.request.body)
        parm=str(response.request.body,'utf-8')#response.request : url 
                                               #response.request.body : parameter
        each_name = ['','창세기','출애굽기','레위기','민수기','신명기  ','여호수아',\
                     '판관기','롯기','사무엘상','사무엘하','열왕기상','열왕기하','역대기상',\
                     '역대기하','애즈라','느헤미아','에스델','욥기','시편','잠언','전도서',\
                     '아가','이사야','에레미야','애가','에제키엘','다니엘','호세아','요엘',\
                     '아모스','오바디야','요나','미가','나흠','하바꾹','스바니야','하깨','즈가리야','말라기']
        #창세기,출애굽기,,,,
        sects = re.findall(r'CtgBCd=\d{1,3}',parm)[0]
        sect = re.sub('CtgBCd=','',sects)
        jangs = re.findall(r'Jang=\d{1,3}',parm)[0]
        jang = re.sub('Jang=','',jangs)

        writedata=[]

        for datalist in textdata:
            datadata = datalist.xpath('*/text()|text()')
            writedata.append("".join(datadata.extract()))    
            print("".join(datadata.extract()))       
  
        filenum = 1  # 성서를 저장할 파일 10개 단위로 분리
        if (int(sect) > 10) and (int(sect) <= 20):
            filenum = 2
        elif (int(sect) > 20) and (int(sect) <= 30):    
            filenum = 3
        elif (int(sect) > 30) and (int(sect) <= 40):    
            filenum = 4   
             
        with open("bible_" + str(filenum) +".txt", "a",  encoding='utf-8') as f:
            #print(str(writedata))
            i=1
            #f.write("창세기 : " + str(sect) + '\n' )
            for k in range(0,len(writedata),2):   #1,3,5,7....:문장  0,2,4,6....:번호
                print(str(i)+'\t'+writedata[k+1])
                #f.write(str(jang) + '\t' +str(i)+'\t'+writedata[k+1]+'\n')
                f.write(sect+'\t' + each_name[int(sect)] + '\t'+str(jang) + '\t' +str(i)+'\t'+writedata[k+1]+'\n')
                i += 1

                                                       