# -*- coding: utf-8 -*-
import scrapy
from book.items import BookItem

class DangdangSpider(scrapy.Spider):
    name = "Dangdang"
    allowed_domains = ["dangdang.com"]
    start_urls = [] # in list window

    rankTypeSuffixes = ['bestsellers','newhotsales']
    rankFreqSuffixes = ['01.00.00.00.00.00-24hours-0-0-2-1','01.00.00.00.00.00-recent30-0-0-2-1']

    for rankTypeSuffix in rankTypeSuffixes:
        for rankFreqSuffix in rankFreqSuffixes:
        	start_urls.append('http://bang.dangdang.com/books/' + rankTypeSuffix + '/'+ rankFreqSuffix)


    def parse(self, response):
        books = response.xpath('//ul[@class="bang_list"]/li')
        items = []
        for i in range(0,19):
            item = BookItem()
            url = books.xpath('.//div[@class="pic"]/a/@href').extract()[i]
            print('foo {}'.format(url))
            yield scrapy.Request(url = url, callback = self.parse_item)

    items = []

    def parse_item(self,response):
        print('bar')
        item = BookItem()

    	name_info = response.xpath('//div[@class="name_info"]')
        item['title'] = name_info.xpath('./h1/@title').extract()[0]
        item['intro'] = name_info.xpath('./h2/span/@title').extract()[0]

        messbox_info = response.xpath('//div[@class="messbox_info"]')
        item['author'] = messbox_info.xpath('.//span[@id="author"]/a/text()').extract()[0]
        item['publisher'] = messbox_info.xpath('.//span[@ddt-area="003"]/a/text()').extract()[0]
        item['star'] = messbox_info.xpath('.//span[@class="star"]/@style').extract()[0]

        item['image'] = response.xpath('//div[@class="pic_info"]//img/@src').extract()[0]
        item['price'] = response.xpath('//div[@class="price_pc"]//p/text()').extract()[0]

        pro_content = response.xpath('//div[@class="pro_content"]')
        item['ISBN'] = pro_content.xpath('./ul[@class="key clearfix"]/li/text()').extract()[9]
        item['tag0'] = pro_content.xpath('.//span[@class="lie"]/a/text()').extract()[0]
        item['tag1'] = pro_content.xpath('.//span[@class="lie"]/a/text()').extract()[1]
        item['tag2'] = pro_content.xpath('.//span[@class="lie"]/a/text()').extract()[2]
        item['link'] = response.url
        item['web'] = 'Dangdang'

        self.items.append(item)
        return self.items
