#coding=utf-8
import requests
from lxml import etree
import json
import threading
import os
class ZhiLian(object):

    def __init__(self,city,job,page):
        self.base_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?'
        self.headers = {'accept':'application/json, text/javascript, */*; q=0.01','referer':'http://jobs.zhaopin.com/521160184251812.htm?ssidkey=y&ss=201&ff=03&sg=c97d627d36ee4071b9971b13828ac63d&so=1',
        'user-agent':'mozilla/5.0 (windoWS NT 10.0; WOW64) apPleWebKit/537.36 (KHTMl, liKe geckO) chrome/62.0.3202.94 safari/537.36',
'X-requested-with':'XmlhTtprequest'}
        self.page = page
        self.params = {'jl':city, "kw":job, 'p':self.page}
    def start(self):
        print "[INFO]正在抓取第%s页" %self.page
        response = requests.get(url=self.base_url, params = self.params, headers=self.headers).content
        # print response
        xml_obj = etree.HTML(response)
        # print xml_obj
        html_list = xml_obj.xpath("//td[@class='zwmc']/div/a/@href")
        for link in html_list:
            # print link
            thread = threading.Thread(target=self.parse_link, args=(link,))
            thread.start()
            # self.parse_link(link)
    def parse_link(self, link):
        response = requests.get(url=link, headers=self.headers).content
        xml_obj = etree.HTML(response)
        content_list = xml_obj.xpath("//ul[@class='terminal-ul clearfix']")
        # 抓取岗位职责和工作地点：
        job_list = xml_obj.xpath("//div[@class='tab-inner-cont'][1]")
        jobname = open("./data/job.json", 'a')
        for job in job_list:
            job_dict = {}
            duty = "".join(job.xpath("./p[2]/text()"))
            ask = "".join(job.xpath("./p[4]/text()"))
            if len(duty) < 5:
                duty = None
            if len(ask) < 5:
                ask = None
            job_dict['duty'] = duty
            job_dict['ask'] = ask
            job_dict['work_place'] = ''.join(job.xpath("./h2/text()")).strip()
            content_job = json.dumps(job_dict, ensure_ascii=False) + '\n'
            jobname.write(content_job.encode("utf-8"))
        jobname.close()
        filename = open("./data/beijing.json", 'a')
        for content in content_list:
            my_dict = {}
            my_dict['money'] = content.xpath("./li[1]/strong/text()")
            my_dict['place'] = content.xpath("./li[2]/strong/a/text()")
            my_dict['status'] = content.xpath("./li[3]/strong/span/text()")
            my_dict['type'] = content.xpath("./li[4]/strong/text()")
            my_dict['age'] = content.xpath("./li[5]/strong/text()")
            my_dict['record'] = content.xpath("./li[6]/strong/text()")
            my_dict['people_number'] = content.xpath("./li[7]/strong/text()")
            my_dict['job_type'] = content.xpath("./li[8]/strong/a/text()")
            # print my_dict
            # my_list.append(my_dict)
            content = json.dumps(my_dict, ensure_ascii=False) + '\n'
            filename.write(content.encode('utf-8'))
        filename.close()
        # print "[INfo]抓取第%s页完成" %self.page


if __name__ == '__main__':
    city = raw_input("请输入要抓取的城市:")
    job = raw_input("请输入要抓取的工作:")
    page_start = raw_input("请输入开始页:")
    page_end = raw_input("请输入结束页:")
    for page in range(int(page_start), int(page_end)+1):
        zhilian = ZhiLian(city, job, str(page))
        zhilian.start()


