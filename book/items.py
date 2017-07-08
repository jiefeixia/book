# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    ISBN      = scrapy.Field()      # *
    title     = scrapy.Field()
    author    = scrapy.Field()
    image     = scrapy.Field()
    publisher = scrapy.Field()
    price	  = scrapy.Field()
    intro     = scrapy.Field()
    star      = scrapy.Field()
    tag0      = scrapy.Field()
    tag1      = scrapy.Field()
    tag2      = scrapy.Field()
    link      = scrapy.Field()
    web		  = scrapy.Field()
    url       = scrapy.Field()


# class RankItem(scrapy.Item):
#     rankTime = scrapy.Field()       # * yyyy-mm or yyyy-mm-dd
#     rankWeb  = scrapy.Field()       # * dangdang jd amazon
#     rankType = scrapy.Field()       # sale new
#     rankFreq = scrapy.Field()       # day month
