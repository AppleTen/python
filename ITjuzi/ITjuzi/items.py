# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):

    # 第一部分：
    # 公司名
    name = scrapy.Field()
    # 口号
    slogan = scrapy.Field()
    # 主页
    home_page = scrapy.Field()
    # 标签
    tag = scrapy.Field()

    # 第二部分：
    # 详细信息
    company_info = scrapy.Field()
    # 公司全称
    company_fullname = scrapy.Field()
    # 成立时间
    company_time = scrapy.Field()
    # 规模
    company_size = scrapy.Field()
    # 运营状态
    company_status = scrapy.Field()


    # 第三部分：
    # 融资信息
    financing  = scrapy.Field()
    #financing_time
    #financing_stage
    #financing_money
    #financing_company

    # 第四部分
    # 团队信息
    team_list  = scrapy.Field()
    #team_name
    #team_title
    #team_info


    # 第五部分
    # 产品信息
    product_list  = scrapy.Field()
    #product_name
    #product_info


    source = scrapy.Field()
    utc_time = scrapy.Field()
