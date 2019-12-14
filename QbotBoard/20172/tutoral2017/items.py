# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
# title,body,date,source,(제목, 본문, link,출처,날짜)
import scrapy

class newsItem(scrapy.Item):
    
    title = scrapy.Field()
    link = scrapy.Field()
    srcname = scrapy.Field()
    date = scrapy.Field()
    #body = scrapy.Field()


