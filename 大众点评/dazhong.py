from selenium import webdriver
from lxml import etree
import time
from selenium.webdriver import ChromeOptions


class CrawlSpider:
    def __init__(self) -> None:
        super().__init__()
        self.options = ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.dirver = webdriver.Chrome(options=self.options)
        self.url = "http://www.dianping.com/beijing"

    def crawl(self):
        self.dirver.get(url=self.url)
        self.dirver.get(url="http://www.dianping.com/shanghai/ch45")
        self.dirver.find_element_by_css_selector("#top-nav > div > div.group.quick-menu > span.login-container.J-login-container > a:nth-child(1)").click()
        time.sleep(10)
        pagetext = self.dirver.page_source
        time.sleep(3)
        # self.dirver.close()
        # print(pagetext)
        html = etree.HTML(pagetext)
        result = html.xpath("//div[@id='shop-all-list']//li")
        for each in result:
            detail_url = each.xpath(".//div[@class='pic']/a/@href")[0]
            self.get_detail(detail_url)

    def get_detail(self, detail_url):
        print(detail_url)
        time.sleep(3)
        time.sleep(3)
        self.dirver.get(detail_url)
        print(self.dirver.get_cookies())
        page_source = self.dirver.page_source
        print(page_source)


if __name__ == "__main__":
    base = CrawlSpider()
    base.crawl()
