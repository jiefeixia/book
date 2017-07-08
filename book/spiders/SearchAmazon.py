# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from book.items import BookItem
import re

class SearchamazonSpider(scrapy.Spider):
    name = "SearchAmazon"
    allowed_domains = ["amazon.cn"]
    start_urls = ['http://www.amazon.cn/']

    def __init__(self, ISBN=None):
        self.ISBN = ISBN
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
        dcap["phantomjs.page.settings.loadImages"] = False
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)


    def parse(self, response):
        self.driver.set_page_load_timeout(20)
        self.driver.get(response.url)

        element = self.driver.find_element_by_id("twotabsearchtextbox")
        element.clear()
        element.send_keys(self.ISBN)
        element.send_keys(Keys.ENTER)

        time.sleep(1)

        url = self.driver.find_element_by_xpath('//li[@id="result_0"]//a[@class="a-link-normal a-text-normal"]/a').get_attribute("href")
        # self.driver.switch_to_window(self.driver.window_handles[1])

        # =====================================================================

        self.driver.get(url)
        item = BookItem()

    	booksTitle = self.driver.find_element_by_xpath('//div[@id="booksTitle"]')
        item['title'] = booksTitle.find_element_by_xpath('.//span[@id="productTitle"]').text
        item['author'] = booksTitle.find_element_by_xpath('.//span[@class="author notFaded"]/a').text

        detail_bullets_id = self.driver.find_element_by_xpath('//div[@id="detail_bullets_id"]//ul')
        item['publisher'] = detail_bullets_id.find_elements_by_xpath('.//li')[0].text
        item['ISBN'] = detail_bullets_id.find_elements_by_xpath('.//li')[5].text
        star = detail_bullets_id.find_element_by_xpath('.//span[@class="swSprite s_star_4_5 "]').get_attribute("title")
        item['star'] = float(re.findall(re.compile(r"(\d+(\.\d+)?)"),star.encode("utf-8"))[0][0])/5*100

        zg_hrsr_ladder = detail_bullets_id.find_element_by_xpath('.//span[@class="zg_hrsr_ladder"]')
        item['tag0'] = zg_hrsr_ladder.find_elements_by_xpath('.//a')[1].text
        item['tag1'] = zg_hrsr_ladder.find_elements_by_xpath('.//a')[2].text
        item['tag2'] = zg_hrsr_ladder.find_element_by_xpath('.//b/a').text

        item['link'] = self.driver.current_url
        item['image'] = self.driver.find_element_by_xpath('//div[@id="main-image-container"]//img').get_attribute("src")
        item['price'] = self.driver.find_element_by_xpath('//span[@class="a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P"]').text

        item['web'] = 'Amazon'

        self.driver.quit()
        return item
