#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
import urllib2
from lxml import etree

class TiebaSpider(object):
    def __init__(self, tieba_name, begin_page, end_page):
        # 1. 不同的User-Agent可能会返回不同的页面
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        #self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}

        self.base_url = "http://tieba.baidu.com"
        self.tieba_name = tieba_name
        self.begin_page = int(begin_page)
        self.end_page = int(end_page)

    def send_request(self, url):
        try:
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            return response.read()
        except Exception, err:
            print "[ERROR]: 请求发送失败.."

    def load_page(self, html):
        html_obj = etree.HTML(html)
        # 每个帖子的链接
        #link_list = html_obj.xpath("//a[@class='j_th_tit']/@href")
        #link_list = html_obj.xpath("//div[@class='threadlist_title pull_left j_th_tit']/a/@href")
        #link_list = html_obj.xpath("//div[@class='threadlist_lz clearfix']/div/a[@class='j_th_tit']/@href")

        # 2. 通过xpath提取数据，如果当前结点取不到数据，就往上一级查找。
        link_list = html_obj.xpath("//div[@class='t_con cleafix']/div/div/div/a/@href")

        for link in link_list:
            html = self.send_request(self.base_url + link)
            #print self.base_url + link
            self.load_image(html)

    def load_image(self, html):
        html_obj = etree.HTML(html)
        link_list = html_obj.xpath("//img[@class='BDE_Image']/@src")

        for link in link_list:
            data = self.send_request(link)
            self.write_image(data, link[-10:])

    def write_image(self, data, filename):
        print "[INFO]： 正在保存" + filename
        with open("./Images/" + filename, "wb") as f:
            f.write(data)





    def start_work(self):
        for page in range(self.begin_page, self.end_page + 1):
            pn = (page - 1) * 50

            keyword = {"kw" : self.tieba_name, "pn" : pn}
            kw_str = urllib.urlencode(keyword)
            full_url = self.base_url + "/f?" + kw_str

            html = self.send_request(full_url)
            self.load_page(html)






if __name__ == "__main__":
    tieba_name = raw_input("请输入贴吧名:")
    begin_page = raw_input("爬取的起始页:")
    end_page = raw_input("爬取的结束页:")

    tieba = TiebaSpider(tieba_name, begin_page, end_page)
    tieba.start_work()
