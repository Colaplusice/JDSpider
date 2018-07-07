# encoding=utf-8
from Config import BEGIN_URL, HEADERS, SECOND_URL
import requests
from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup


class Jindong:
    def __init__(self):
        self.message_list = ['商品名称', '商品编号', '运行内存', '前置摄像头像素', '电池容量', '机身颜色', '价格']
        self.begin_queue = [BEGIN_URL, SECOND_URL]
        self.headers = HEADERS
        self.href_queue = []

    # 得到所有的商品链接
    def get_href(self):
        driver = webdriver.Firefox()
        queue = self.begin_queue
        while queue:
            url = queue.pop()
            print('this is the main url:{}'.format(url))
            driver.get(url)
            time.sleep(3)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
            # response=requests.get(url=url,headers=self.headers)
            # response.encoding=response.apparent_encoding
            self.parse_html(html)

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        result = soup.find_all('li', {'class': 'gl-item'})

        for each in result:
            a = each.find('a')
            url = 'https:{}'.format(a['href'])
            print(url)
            price = each.find('div', {'class': 'p-price'}).find('i').string
            self.href_queue.append((price, url))
        print('href queue 的长度{}'.format(len(self.href_queue)))

    def get_single_message(self):
        url_queue = self.href_queue
        list_queue = []
        while url_queue:
            url_message = url_queue.pop()
            url = url_message[1]
            print('url:{}'.format(url))
            time.sleep(1)

            response = requests.get(url=url, headers=self.headers)
            result_list = self.parse_single_html(response.text)
            result_list.append(url_message[0])
            print('抓取成功')
            result_tuple = tuple(result_list)
            list_queue.append(result_tuple)
            self.write_in_csv(result_tuple)
        return list_queue

    def parse_single_html(self, html):
        result_list = []
        key_list = []
        soup = BeautifulSoup(html, 'html.parser')
        all_info = soup.find_all('div', {'class': 'itemInfo-wrap'})
        # name
        # for each in all_info:
        #     name = each.find('div', {'class': 'sku-name'})
        #     print name

        # info list
        para = soup.find('ul', {'class': 'parameter2 p-parameter-list'})
        # print all_message
        for each in para:
            print(each)
            result = str(each.string)
            result = ''.join(result.split(' '))
            if '：' in result:
                print(result)
                message_list = result.split('：')
                value = message_list[1]
                key = message_list[0]
                if key in self.message_list:
                    result_list.append(value)
        return result_list

    def write_in_csv(self, result_tuple):
        with open('message.csv', 'a')as opener:
            writer = csv.writer(opener)
            writer.writerow(result_tuple)
            print(result_tuple)
            print('写入成功')

    def write_Html(self, html):
        with open('message.html', 'w')as opener:
            opener.write(html)


jd = Jindong()

jd.get_href()
dicts_queue = jd.get_single_message()
