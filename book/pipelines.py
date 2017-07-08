# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BookPipeline(object):
    def process_item(self, item, spider):
	item['price'] = filter(lambda ch: ch in ‘0123456789.’, item['price'])
	item['star'] = filter(lambda ch: ch in ‘0123456789.’, item['star'])  # in 100%
	item['ISBN'] = filter(str.isdigit,item['ISBN'].encode('utf-8'))
        return item
