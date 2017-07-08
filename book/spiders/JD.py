# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from book.items import BookItem
import re


class JdSpider(scrapy.Spider):
    name = "JD"
    allowed_domains = ["jd.com"]
    start_urls = ['http://book.jd.com/']
    rankTypeSuffixes = ['0-0-0','0-1-0'] # 0-0-0 means bestsellers, 0-1-0 means new newhotsales
    rankFreqSuffixes = ['10001','10003'] # 10001 means ranking list of 24 hours, 10003 means ranking list of 30 days

    for rankTypeSuffix in rankTypeSuffixes:
        for rankFreqSuffix in rankFreqSuffixes:
        	start_urls.append('http://book.jd.com/booktop/' + rankTypeSuffix + '.html?category=1713-' + rankTypeSuffix + '-' + rankFreqSuffix + '-1#comfort')

    def parse(self, response):
        books = response.xpath('//div[@class="m m-list"]')
        items = []
        for i in range(0,19):
            item = BookItem()
            url = 'http:' + books.xpath('.//li/div[@class="p-img"]/a/@href').extract()[i]
            print(url)
            # yield scrapy.Request(url = 'http:'+ url, callback = self.parse_item)
            item = PhantomJSCrawl(url)
            items.append(item)
        return items

def PhantomJSCrawl(url):
    driver = webdriver.Chrome()
    driver.get(url)

    item = BookItem()
    item['title'] = driver.find_element_by_xpath('//div[@id="name"]/h1').text
    item['author'] = driver.find_element_by_xpath('//div[@id="name"]/div[@class="p-author"]/a').text
    item['image'] = driver.find_element_by_xpath('//div[@id="preview"]//img').get_attribute('src')

    price = driver.find_element_by_id("jd-price").text
    item['price'] = re.findall(re.compile(r"(\d+(\.\d+)?)"), price.encode("utf-8"))[0][0]

    parameter2 = driver.find_element_by_id('parameter2')
    item['publisher'] = parameter2.find_elements_by_xpath('.//li')[0].get_attribute('title')
    item['ISBN'] = parameter2.find_elements_by_xpath('.//li')[1].get_attribute('title')

    breadcrumb = driver.find_element_by_xpath('//div[@class="breadcrumb"]')
    item['tag0'] = breadcrumb.find_elements_by_xpath('.//a')[0].text
    item['tag1'] = breadcrumb.find_elements_by_xpath('.//a')[1].text
    item['tag2'] = breadcrumb.find_elements_by_xpath('.//a')[2].text

    item['link'] = url
    item['web'] = 'JD'

    driver.quit()
    return item

    # def parse_item(self,response):
    #
    #     item = BookItem()
    #
    # 	  name = response.xpath('//div[@id="name"]')
    #     item['title'] = name.xpath('./h1/text()').extract()[0]
    #     item['author'] = name.xpath('.//div[@class="p-author"]/a/text()').extract()[0]
    #
    #     image = item['image'] = response.xpath('//div[@id="preview"]//img/@src').extract()[0]
    #     item['image'] = 'http://' + image.encode("utf-8")
    #
    #
    #     price = response.xpath('//strong[@class="p-price"]/text()').extract()[0]
    #     item['price'] = re.findall(re.compile(r"(\d+(\.\d+)?)"), price.encode("utf-8"))[0][0]
    #
    #     parameter2 = response.xpath('//ul[@id="parameter2"]')
    #     item['publisher'] = parameter2.xpath('.//li/@title').extract()[0]
    #     item['ISBN'] = parameter2.xpath('.//li/@title').extract()[1]
    #
    #     breadcrumb = response.xpath('//div[@class="breadcrumb"]')
    #     item['tag0'] = breadcrumb.xpath('.//a/text()').extract()[0]
    #     item['tag1'] = breadcrumb.xpath('.//a/text()').extract()[1]
    #     item['tag2'] = breadcrumb.xpath('.//a/text()').extract()[2]
    #
    #     item['link'] = response.url
    #     item['web'] = 'JD'
    #
    #     self.items.append(item)
    #     return self.items
