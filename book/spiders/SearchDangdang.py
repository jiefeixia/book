# -*- coding: utf-8 -*-
import scrapy


class SearchdangdangSpider(scrapy.Spider):
    name = "SearchDangdang"
    allowed_domains = ["dangdang.com"]
    start_urls = ['http://www.dangdang.com/']

    def __init__(self, ISBN=None):
        self.ISBN = ISBN
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
        dcap["phantomjs.page.settings.loadImages"] = False
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)


    def parse(self, response):
        self.driver.set_page_load_timeout(20)
        self.driver.get(response.url)

        element = self.driver.find_element_by_id("key_S")
        element.clear()
        element.send_keys(self.ISBN)
        element.send_keys(Keys.ENTER)

        time.sleep(1)

        url = self.driver.find_element_by_find_element_by_xpath('//ul[@id="component_0__0__6612"]//li[@class="line1"]/a').get_attribute("href")
        # self.driver.switch_to_window(self.driver.window_handles[1])

        self.driver.get(url)
        item = BookItem()
    	name_info = self.driver.find_element_by_xpath('//div[@class="name_info"]')
        item['title'] = name_info.find_element_by_xpath('./h1').get_attribute("title")
        item['intro'] = name_info.find_element_by_xpath('./h2/span').get_attribute("title")

        messbox_info = self.driver.find_element_by_xpath('//div[@class="messbox_info"]')
        item['author'] = messbox_info.find_element_by_xpath('.//span[@id="author"]/a').text
        item['publisher'] = messbox_info.find_element_by_xpath('.//span[@ddt-area="003"]/a').text
        item['star'] = messbox_info.find_element_by_xpath('.//span[@class="star"]').get_attribute("style")

        item['image'] = self.driver.find_element_by_xpath('//div[@class="pic_info"]//img/').get_attribute("src")
        item['price'] = self.driver.find_element_by_xpath('//div[@class="price_pc"]//p').text

        pro_content = self.driver.find_element_by_xpath('//div[@class="pro_content"]')
        item['ISBN'] = pro_content.find_elements_by_xpath('./ul[@class="key clearfix"]/li/text()')[9].text
        item['tag0'] = pro_content.find_elements_by_xpath('.//span[@class="lie"]/a')[0].text
        item['tag1'] = pro_content.find_elements_by_xpath('.//span[@class="lie"]/a/text()')[1].text
        item['tag2'] = pro_content.find_elements_by_xpath('.//span[@class="lie"]/a/text()')[2].text

        item['link'] = self.driver.current_url
        item['web'] = 'Dangdang'

        self.driver.quit()
        return item
