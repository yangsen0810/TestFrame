# author:杨森
# date: 2019/11/2 13:30
# file_name: 爬取小说网站
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import requests

def get_url(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    driver.find_element_by_xpath("//ul[@class='books-group-4']/li[2]").click()
    time.sleep(3)
    # 点击开始阅读
    driver.find_element_by_xpath("//section[@class='cover-fn-buttons']/a[@class='bs-button button-fill button-block']").click()
    time.sleep(3)
    return driver.current_url,driver.page_source

def get_next(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    driver.maximize_window()
    time.sleep(3)
    return driver.current_url,driver.page_source

def get_content(html):
    soup = BeautifulSoup(html,"lxml")
    result = soup.select("div.read-body div")
    content = ""
    for each in result:
        content += each.get_text()
    return content


if __name__ == "__main__":
    url = "http://t.shuqi.com/route.php?"
    url,html = get_url(url)
    pat_number = re.compile("cid/(.*?)/")
    number = pat_number.search(url).group(1)
    number = int(number)
    url = url.split("cid")[0]
    content_list = []
    for i in range(10):
        if i == 0:
            content = get_content(html)
            content_list.append(content)
        else:
            number += 1
            new_url = url+f"cid/{str(number)}/ct/read"
            cru_url,html = get_next(new_url)
            time.sleep(3)
            content = get_content(html)
            content_list.append(content)
    with open("./novel.txt", "w",encoding="utf-8") as f:
          f.write("".join(content_list))

