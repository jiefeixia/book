# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from book.items import BookItem
import re

class AmazonSpider(scrapy.Spider):
    name = "Amazon"
    allowed_domains = ["www.amazon.cn"]
    start_urls = []

    rankTypeSuffixes = ['bestsellers/books/ref=sv_b_3','new-releases/books/ref=zg_bs_tab_t_bsnr']
    # no rankFreqSuffixes, only contain ranking list for 24 hours

    for rankTypeSuffix in rankTypeSuffixes:
        start_urls.append('https://www.amazon.cn/gp/' + rankTypeSuffix)

    def parse(self, response):
        for i in range(0,19):
            items = []
            item = BookItem()
            book = response.xpath('//div[@id="zg_left_col1"]//div[@class="zg_itemRow"]//div[@class="a-fixed-left-grid-col a-col-left"]/a/@href').extract()[i]
            url = 'https://www.amazon.cn' + str(book)

            self.headers = {'ccept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',\
                            'Accept-Encoding':'gzip,deflate,sdch',\
                            'Accept-Language':'zh-CN,zh;q=0.8',\
                            'Cache-Control':'max-age=0',\
                            'Connection':'keep-alive',\
                            'referer': url,\
                            'user-agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',\
                            }

            yield Request(url = url, headers = self.headers, callback = self.parse_item)

    items = []

    def parse_item(self,response):
        item = BookItem()

    	booksTitle = response.xpath('//div[@id="booksTitle"]')
        item['title'] = booksTitle.xpath('.//span[@id="productTitle"]/text()').extract()[0]
        item['author'] = booksTitle.xpath('.//span[@class="author notFaded"]/a/text()').extract()[0]

        detail_bullets_id = response.xpath('//div[@id="detail_bullets_id"]//ul')
        item['publisher'] = detail_bullets_id.xpath('.//li/text()').extract()[0]
        item['ISBN'] = detail_bullets_id.xpath('.//li/text()').extract()[5]
        star = detail_bullets_id.xpath('.//span[@class="swSprite s_star_4_5 "]/@title').extract()[0]
        item['star'] = float(re.findall(re.compile(r"(\d+(\.\d+)?)"),star.encode("utf-8"))[0][0])/5*100
        zg_hrsr_ladder = detail_bullets_id.xpath('.//span[@class="zg_hrsr_ladder"]')
        item['tag0'] = zg_hrsr_ladder.xpath('.//a/text()').extract()[1]
        item['tag1'] = zg_hrsr_ladder.xpath('.//a/text()').extract()[2]
        item['tag2'] = zg_hrsr_ladder.xpath('.//b/a/text()').extract()[0]

        item['link'] = response.url
        item['image'] = response.xpath('//div[@id="main-image-container"]//img/@src').extract()[0]
        item['price'] = response.xpath('//span[@class="a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P"]/text()').extract()[0]

        item['web'] = 'JD'

        self.items.append(item)
        return self.items
