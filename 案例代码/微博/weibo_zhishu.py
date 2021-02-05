# -*- coding: utf-8 -*-
# @Time    : 2020/2/5 14:19
# @Author  : lx
# @IDE ：PyCharm
import requests
import json
import re

# TODO 微博移动版指数

class WeiboZhishu():
    def __init__(self):

        self.search_word_api = 'https://data.weibo.com/index/ajax/newindex/searchword'
        self.get_data_url = 'https://data.weibo.com/index/ajax/newindex/getchartdata'
        self.headers = {
            'Referer': 'https://data.weibo.com/index/newindex?visit_type=trend&wid=120190311105634317618',
            'Origin': 'https://data.weibo.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36',
                  }


    def search_wid(self,program_name):
        data_search = {
            "word": program_name,
                      }

        search_text = requests.post(self.search_word_api, data=data_search, headers=self.headers).text
        search_json = json.loads(search_text)
        if search_json['code'] ==100:
            wid = search_json['html']
            wid = re.findall('wid="(.*?)"', wid, re.S)[0]
            return wid
        else:
            return None


    def req_post(self,url,data,proxy_result):
        if proxy_result:
            req_post_text = requests.post(url=url,data=data,headers = self.headers,proxies=proxy_result).text
            return req_post_text
        else:
            req_post_text = requests.post(url=url,data=data,headers = self.headers).text
            return req_post_text


    def get_data(self,program_name,timer):
        wid = self.search_wid(program_name)
        if not wid:
            return -1,-1,-1
        data_get = {
            'dateGroup': timer,
            'wid': wid
                    }
        data_text = requests.post(self.get_data_url, data=data_get,headers=self.headers).text
        json_text = json.loads(data_text)
        if json_text['code'] == 100:
            x = json_text['data'][0]['trend']['x']
            end_x = json_text['data'][0]['trend']['end_x']
            s = json_text['data'][0]['trend']['s']
            return x,s[-1]



zhishu = WeiboZhishu()
x,s = zhishu.get_data('乐队的夏天','1day')
if x ==-1:
    print("请求有误---请检查节目是否被微博指数收录")
else:
    print(s)
