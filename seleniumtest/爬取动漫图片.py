# author:杨森
# date: 2019/10/26 15:43
# file_name: 爬取动漫图片
from selenium import webdriver
import time
import requests
import re
import uuid

# 获取所有的图片
def getallurl(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.maximize_window()
        time.sleep(1)
        # 获取图片的连接
        all_li = driver.find_elements_by_css_selector("div.tab_box ul.clearfix > li")[0:24]
        print(len(all_li))
        # 遍历所有的图片
        for each_link in all_li:
            img_link = each_link.find_element_by_xpath("./a").get_attribute("href")
            downimg(img_link)
    except Exception as e:
        print(e)
        print("请求错误")

def downimg(img_link):
    response = requests.get(img_link)
    html = response.text
     # 使用re模块完成图片连接的获取
    pat_img = re.compile('<img.*?class="pic-large".*?src="(.*?)".*?alt="(.*?)"')
    img_link = pat_img.search(html, re.M | re.S).group(1)
    img_name = pat_img.search(html,re.M | re.S).group(2)
    response = requests.get(img_link)
    with open(f"../images/{img_name}{uuid.uuid4().hex}.jpg","wb") as f:
        f.write(response.content)
    # 判断下一页的地址是否小于自身的地址
    pat_next = re.compile('<div.*?class="pic-next-img"><a.*?href="(.*?)">',re.M | re.S)
    next_page = pat_next.search(html, re.M | re.S).group(1)
    if len(pat_next.search(html, re.M | re.S).group(1)) == 53:
        downimg(next_page)
    else:
        return None


if __name__ == "__main__":
    url = "http://www.win4000.com/zt/dongman.html"
    while True:
        start_num = int(input("请输入开始页数"))
        end_num = int(input("请输入结束页数"))
        if 1 <= start_num <= 5 and start_num<=end_num<=5:
            break
    for each_page in (start_num,end_num):
        url = "http://www.win4000.com/zt/dongman_"+str(each_page)+".html"
        getallurl(url)
