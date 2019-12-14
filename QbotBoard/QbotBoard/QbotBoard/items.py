# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#class QbotboardItem(scrapy.Item):
class HelloItem(scrapy.Item):
    # define the fields for your item here like:
    cate = scrapy.Field()
    Qtitle = scrapy.Field()
    Qtitle_content = scrapy.Field()
    answer = scrapy.Field()
    link_url = scrapy.Field(serializer=str)
    #writedate = scrapy.Field()        
    #pass
