# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from book.items import BookItem
import re
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SearchjdSpider(scrapy.Spider):
    name = "SearchJD"
    allowed_domains = ["jd.com"]
    start_urls = ['https://book.jd.com']


    def __init__(self, ISBN=None):
        self.ISBN = ISBN
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
        dcap["phantomjs.page.settings.loadImages"] = False
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)


    def parse(self, response):
        self.driver.set_page_load_timeout(20)
        self.driver.get(response.url)

        element = self.driver.find_element_by_id("key")
        element.clear()
        element.send_keys(self.ISBN)
        element.send_keys(Keys.ENTER)

        time.sleep(1)

        url = self.driver.find_element_by_xpath('//ul[@class="gl-warp clearfix"]//div[@class="p-img"]/a').get_attribute("href")
        # self.driver.switch_to_window(self.driver.window_handles[1])

        self.driver.get(url)
        item = BookItem()
        item['title'] = self.driver.find_element_by_xpath('//div[@id="name"]/h1').text
        item['author'] = self.driver.find_element_by_xpath('//div[@id="name"]/div[@class="p-author"]/a').text
        item['image'] = self.driver.find_element_by_xpath('//div[@id="preview"]//img').get_attribute('src')

        price = self.driver.find_element_by_id("jd-price").text
        item['price'] = re.findall(re.compile(r"(\d+(\.\d+)?)"), price.encode("utf-8"))[0][0]

        parameter2 = self.driver.find_element_by_id('parameter2')
        item['publisher'] = parameter2.find_elements_by_xpath('.//li')[0].get_attribute('title')
        ISBN = parameter2.find_elements_by_xpath('.//li')[1].get_attribute('title')
        item['ISBN'] = filter(str.isdigit, ISBN.encode("utf-8")).decode("utf-8")

        breadcrumb = self.driver.find_element_by_xpath('//div[@class="breadcrumb"]')
        item['tag0'] = breadcrumb.find_elements_by_xpath('.//a')[0].text
        item['tag1'] = breadcrumb.find_elements_by_xpath('.//a')[1].text
        item['tag2'] = breadcrumb.find_elements_by_xpath('.//a')[2].text

        item['link'] = self.driver.current_url
        item['web'] = 'JD'

        self.driver.quit()
        return item
