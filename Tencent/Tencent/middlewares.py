# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from settings import USER_AGENT_LIST as ua_list
import random

class UserAgentMiddleware(object):
    """
        给每一个请求随机切换一个User-Agent
    """
    def process_request(self, request, spider):
        user_agent = random.choice(ua_list)
        request.headers['User-Agent'] = user_agent

        #print request.headers['User-Agent']

class ProxyMiddleware(object):
    """
        给每一个请求随机切换一个代理IP
    """
    #proxy_list = ['http://120.26.167.140:16816', 'http://120.26.167.140:16816']
    proxy_list = ['http://mr_mao_hacker:sffqry9r@120.26.167.140:16816', 'http://mr_mao_hacker:sffqry9r@120.26.167.140:16816']

    def process_request(self, request, spider):
        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = proxy

