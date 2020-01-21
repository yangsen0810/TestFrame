import requests
from fontTools.ttLib import TTFont
from fake_useragent import UserAgent
from lxml import etree
from bs4 import BeautifulSoup
import time
import re
from Dictmapname import DictMap
import random


class CrawlSpider:

    def __init__(self, url) -> None:
        super().__init__()
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip,deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': '_lxsdk_cuid=16c19704861c8-05e2ad89692f0f-c343162-1fa400-16c19704861c8;_lxsdk=16c19704861c8-05e2ad89692f0f-c343162-1fa400-16c19704861c8;_hc.v=11ff6ffb-2a80-d450-6f3b-81beb5474db7.1563794885;s_ViewType=10;aburl=1;Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1563796204;Hm_lvt_4c4fc10949f0d691f3a2cc4ca5065397=1563978129;cityInfo=%7B%22cityId%22%3A7%2C%22cityName%22%3A%22%E6%B7%B1%E5%9C%B3%22%2C%22provinceId%22%3A0%2C%22parentCityId%22%3A0%2C%22cityOrderId%22%3A0%2C%22isActiveCity%22%3Afalse%2C%22cityEnName%22%3A%22shenzhen%22%2C%22cityPyName%22%3Anull%2C%22cityAreaCode%22%3Anull%2C%22cityAbbrCode%22%3Anull%2C%22isOverseasCity%22%3Afalse%2C%22isScenery%22%3Afalse%2C%22TuanGouFlag%22%3A0%2C%22cityLevel%22%3A0%2C%22appHotLevel%22%3A0%2C%22gLat%22%3A0%2C%22gLng%22%3A0%2C%22directURL%22%3Anull%2C%22standardEnName%22%3Anull%7D;ctu=2b7c08185b82e8ae4df8f87aec20348bf116a030d673eff3a9b54efd230bd068;ua=%E4%BC%8A%E5%8D%A1%E9%B2%81%E6%96%AF;cy=2;cye=beijing;_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic;uamo=13622051920;_lxsdk_s=16c40465ce1-90c-b2-244%7C%7C59;lgtoken=078fec8b0-6a63-4c88-a368-41f57b0b2e1f;dper=46ff226a44351c57f61b4d66b0808f67bbf2e7d28de0fc3c302206817496e522b7e4a640ee66b8b1d0cb5f6210dcaa60975820fe362bca5418135d1b64c9db57b6bbc5e1088dda31ba9076facc2e4fb8fd218c36cc8294645208e58936b97033;ll=7fd06e815b796be3df069dec7836c3df',
            'Host': 'www.dianping.com', 'Pragma': 'no-cache', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/75.0.3770.142Safari/537.36', }

        self.header2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip,deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.dianping.com', 'Pragma': 'no-cache', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/75.0.3770.142Safari/537.36',
            'If-Modified-Since': 'Mon, 20 Jan 2020 03:51: 07 GMT',
            'If-None-Match': "b25b59e09efbdd830a632774d14254b4",
            'Referer': 'http://www.dianping.com/shanghai/ch45'
        }
        self.address = ""
        self.types = ""
        self.address_rea = ""
        self.address_load = ""
        self.url = url

    def font_handle(self):
        '''下载字体文件'''
        # pat = re.compile(r"\n           url\('(.*?.woff)'\).*?format\('woff'\)", re.M | re.S)
        down_url = {
            "address": " http://s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/78dc3365.woff",
            "num": "http://s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/d283d002.woff"
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        for name, url in down_url.items():
            print(name, url)
            ttf = requests.get(url, stream=True, headers=headers)
            with open(f'./{name}.woff', 'wb') as pdf:
                for chunck in ttf.iter_content(chunk_size=1024):
                    if chunck:
                        pdf.write(chunck)
            if name == "address":
                self.font_address = TTFont(f'./{name}.woff')
                self.font_address.saveXML('./地址.xml')
            elif name == "num":
                self.font_num = TTFont(f'./{name}.woff')
                self.font_num.saveXML(f'./电话.xml')

    def get_url(self):
        ua = UserAgent()
        # print(ua.chrome)
        response = requests.get(url=self.url, headers=self.header)
        # print(response.content.decode("utf-8"))
        # print(response.text)
        # 提取所有的链接
        html = etree.HTML(response.content.decode("utf-8"))
        all_link = html.xpath("//div[@id='shop-all-list']//div[@class='pic']/a/@href")
        for each in all_link:
            self.get_detail(each)
            time.sleep(1)

    def get_detail(self, link_src):
        base = DictMap()
        cookie_list = base.get_cookie()
        self.header2["Cookie"] = random.choice(cookie_list)
        detail = requests.get(url=link_src, headers=self.header2)
        result = detail.content.decode("utf-8")
        # print(result)
        # 使用bs4 进行提取
        soup = BeautifulSoup(result, "lxml")
        all_info = soup.select("div[class='breadcrumb'] > a")
        for ind, link in enumerate(all_info):
            if ind == 0:
                try:
                    self.address = link.get_text()
                except:
                    self.address = ""
            elif ind == 1:
                try:
                    self.types = link.get_text()
                except:
                    self.types = ""
            elif ind == 2:
                try:
                    self.address_rea = link.get_text()
                except:
                    self.address_rea = ""
            elif ind == 3:
                try:
                    self.address_load = link.get_text()
                except:
                    self.address_load = ""
            else:
                pass
        # 打印地区
        print(self.address + self.types + self.address_rea + self.address_load)
        # 打印店名
        try:
            store_name = soup.select_one("div[class='breadcrumb'] > span").get_text()
            print(store_name)
        except Exception as e:
            print(e)
            print("未找到店名")
            store_name = ""
            print(store_name)
        # 针对地址采用的加密需要采用需要进行破解
        # 提取地址
        pat_address = re.compile(
            r'<span class="item" itemprop="street-address" id="address">(.*?)</span>', re.M | re.S)
        try:
            address_code = pat_address.search(result).group(1)
        except Exception as e:
            print(e)
            print("未进行匹配到地址")
            return None
        # print(address_code)
        # 进行二次提取
        pat_address_code = re.compile(r'<e class="address">(.*?)</e>')
        pat_num_code = re.compile(r'<d class="num">(.*?)</d>')
        reper_address_code = pat_address_code.findall(address_code)
        reper_num_code = pat_num_code.findall(address_code)
        time.sleep(1)
        reper_num_res = self.replace_num(reper_num_code)
        time.sleep(1)
        # 进行代码的替换
        reper_add_res = self.replace_address(reper_address_code)
        for each_addr in reper_add_res:
            for ind, each_reper in enumerate(reper_address_code):
                if address_code.find(f'<e class="address">{each_reper}</e>') >= 0:
                    address_code = address_code.replace(f'<e class="address">{each_reper}</e>', each_addr, 1)
                    reper_address_code.pop(ind)
                    break
        # print(address_code)
        # 进行数字的代码替换
        for each_num in reper_num_res:
            for ind, each_reper_num in enumerate(reper_num_code):
                if address_code.find(f'<d class="num">{each_reper_num}</d>') >= 0:
                    address_code = address_code.replace(f'<d class="num">{each_reper_num}</d>', each_num, 1)
                    reper_num_code.pop(ind)
                    break
        print(address_code)
        # 针对电话加密进行解密
        pat_phone_num = re.compile('<span class="info-name">电话：</span>(.*?)</p>')
        all_phone_num = pat_phone_num.search(result).group(1)
        pat_get_num = re.compile('<d class="num">(.*?)</d>')
        num_code = pat_get_num.findall(all_phone_num)
        phone_num = self.replace_num(num_code)
        for each_num in phone_num:
            for ind, each_reper_num in enumerate(num_code):
                if all_phone_num.find(f'<d class="num">{each_reper_num}</d>') >= 0:
                    all_phone_num = all_phone_num.replace(f'<d class="num">{each_reper_num}</d>', each_num, 1)
                    num_code.pop(ind)
                    break
        all_phone_num = all_phone_num.replace(" &nbsp;", ";")
        print(all_phone_num)

    def replace_address(self, address_code):
        address_map = DictMap()
        add_map = address_map.get_address_dict()
        result_list = list()
        for each in address_code:
            each_name = each.replace("&#x", "uni")[:7]
            # print(each_name)
            result = str(self.font_address.getGlyphID(each_name))
            if result in add_map.keys():
                result_list.append(add_map[result])
        # print(result_list)
        return result_list

    def replace_num(self, num_code):
        num_dict_map = DictMap()
        num_map = num_dict_map.get_num_dict()
        result_list = list()
        for each in num_code:
            each_name = each.replace("&#x", "uni")[:7]
            # print(each_name)
            result = str(self.font_num.getGlyphID(each_name))
            if result in num_map.keys():
                result_list.append(num_map[result])
        return result_list


if __name__ == "__main__":
    ind = ""
    url = "http://www.dianping.com/shanghai/ch45/pind"
    base = CrawlSpider(url)
    # 下载字体加密文件
    # font_handle()
    # print(get_url())
    for each in range(1, 51):
        base2 = CrawlSpider(url)
        base2.font_handle()
        base2.url = base2.url.replace("ind",str(each))
        print(base2.url)
        time.sleep(1)
        base2.get_url()
