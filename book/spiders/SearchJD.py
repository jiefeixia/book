# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from book.items import BookItem
import re

class SearchjdSpider(scrapy.Spider):
    name = "SearchJD"
    allowed_domains = ["jd.com"]
    start_urls = ['https://book.jd.com']

    def search(self, response):
        driver = webdriver.Chrome().get(response.url)

        element = driver.find_element_by_id("key")
        element.clear()
        element.send_keys("9787555107408")
        element.send_keys(Keys.ENTER)

        url = driver.find_element_by_xpath('//ul[@class="gl-warp clearfix"]//div[@class="p-img"]/a').get_attribute("href")
        driver.quit()

        item = PhantomJSCrawl(url)

        return item


def PhantomJSCrawl(url):
    driver = webdriver.Chrome().get(url)

    item = BookItem()
    item['title'] = driver.find_element_by_xpath('//div[@id="name"]/h1').text
    item['author'] = driver.find_element_by_xpath('//div[@id="name"]/div[@class="p-author"]/a').text
    item['image'] = driver.find_element_by_xpath('//div[@id="preview"]//img').get_attribute('src')

    price = driver.find_element_by_id("jd-price").text
    item['price'] = re.findall(re.compile(r"(\d+(\.\d+)?)"), price.encode("utf-8"))[0][0]

    parameter2 = driver.find_element_by_id('parameter2')
    item['publisher'] = parameter2.find_elements_by_xpath('.//li')[0].get_attribute('title')
    ISBN = parameter2.find_elements_by_xpath('.//li')[1].get_attribute('title')
    item['ISBN'] = filter(str.isdigit, ISBN)

    breadcrumb = driver.find_element_by_xpath('//div[@class="breadcrumb"]')
    item['tag0'] = breadcrumb.find_elements_by_xpath('.//a')[0].text
    item['tag1'] = breadcrumb.find_elements_by_xpath('.//a')[1].text
    item['tag2'] = breadcrumb.find_elements_by_xpath('.//a')[2].text

    item['link'] = url
    item['web'] = 'JD'

    driver.quit()
    return item
