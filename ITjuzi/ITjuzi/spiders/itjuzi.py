# -*- coding=utf-8 -*-

import scrapy
from ITjuzi.items import ItjuziItem
from bs4 import BeautifulSoup

class ItjuziSpider(scrapy.Spider):
    name = "itjuzi"
    allowed_domains = ["itjuzi.com"]

    base_url = "https://www.itjuzi.com/company/"
    offset = 1

    start_urls = [base_url + str(offset)]

    headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language" : "zh-CN,zh;q=0.9,en;q=0.8",
        "Cookie" : "gr_user_id=145c121f-fb8c-4a8e-8190-231596b3f2d7; MEIQIA_EXTRA_TRACK_ID=0upVCH2EUiLusLRQf3MWQiShmmu; identity=18515668440%40test.com; remember_code=awi7EV5oE5; unique_token=408791; acw_tc=AQAAAFSXLVQAtgcAK3CCDjZFK6vReuKS; _gat=1; session=9481f7670ab8fc61957773e00f176774bf5cfaa6; _ga=GA1.2.1588476138.1507779389; _gid=GA1.2.1622026763.1510827738; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1510827738,1510880168,1510885120; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1510891010",
        "Host" : "www.itjuzi.com",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url = url, headers = self.headers, callback = self.parse)


    def parse(self, response):
        if response.status == 200:

            soup = BeautifulSoup(response.body, "lxml")
            item = ItjuziItem()

            # 第一部分：公司简介信息
            cpy1 =  soup.find("div", class_='infoheadrow-v2')
            if cpy1:
                # 1. 根据结点标签进行判断，如果不为None，表示有数据则进行取值，否则直接返回None
                content = cpy1.find(class_="seo-important-title")
                item['name'] = content.contents[0].strip() if content else content

                # 2. 写try except 异常判断处理
                try:
                    item['slogan'] = cpy1.find("h2").get_text()
                except:
                    item['slogan'] = None



                item['home_page'] = cpy1.find(class_="link-line").find_all('a')[-1].get_text().strip()

                item['tag'] = cpy1.find(class_="tagset").get_text().strip().replace("\n", " ")


            # 第二部分：公司详细信息
            cpy2 = soup.find(class_='block-inc-info')
            if cpy2:
                item['company_info'] = cpy2.find_all(class_='block')[1].get_text().strip()

                item['company_fullname'] = cpy2.find("h2").get_text().strip()

                item['company_time'] = cpy2.find_all("h3")[0].get_text().strip()

                item['company_size'] = cpy2.find_all("h3")[1].get_text().strip()
                item['company_status'] = cpy2.find_all("span")[-1].get_text().strip()




            # 第三部分：融资信息
            cpy3 =  soup.find(class_='list-round-v2')
            if cpy3:
                tr_list = cpy3.find_all("tr")
                if len(cpy3.find_all("td")) > 1:
                    # 保存所有融资信息的列表
                    tr_item_list = []
                    for tr in tr_list:
                        # 每个字典都是一条融资信息
                        tr_item = {}
                        tr_item['financing_time'] = tr.find_all("td")[0].get_text().strip()
                        tr_item['financing_stage'] = tr.find_all("td")[1].get_text().strip()
                        tr_item['financing_money'] = tr.find_all("td")[2].get_text().strip()
                        tr_item['financing_company'] = tr.find_all("td")[3].get_text().strip().replace("\n", " ")

                        tr_item_list.append(tr_item)

                    item['financing'] = tr_item_list
                else:
                    item['financing'] = None



            # 第四部分：成员信息
            cpy4 = soup.find(class_='team-list')
            if cpy4:
                li_list = cpy4.find_all("li")
                if li_list:

                    li_item_list = []
                    for li in li_list:
                        li_item = {}
                        li_item['team_name'] = li.find_all("div")[1].get_text().strip()
                        li_item['team_title'] = li.find_all("div")[2].get_text().strip()
                        li_item['team_info'] = li.find_all("div")[3].get_text().strip()

                        li_item_list.append(li_item)


                    item['team_list'] = li_item_list
                else:
                    item['team_list'] = None




            cpy5 = soup.find(class_='product-list')
            if cpy5:
                li_list = cpy5.find_all("li")
                if li_list:

                    li_item_list = []
                    for li in li_list:
                        li_item = {}
                        li_item['product_name'] = li.find(class_='product-name').get_text().strip()

                        li_item['product_info'] = li.find("div").get_text().strip()

                        li_item_list.append(li_item)

                    item['product_list'] = li_item_list
                else:
                    item['product_list'] = None


            yield item

        self.offset += 1
        yield scrapy.Request(self.base_url + str(self.offset), callback = self.parse)

