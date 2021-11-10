# -*- coding: utf-8 -*-
# @Time    : 2021/2/23 9:50
import datetime
import re
import threading
import time
import requests
from lxml import etree
from lxpy import DateGo


class ZhenfucaigouSpider():
    def __init__(self,keyword='',bidType=0): # 0 -> 所有类型
        self.url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1'
        self.keyword = keyword
        self.bidType = bidType
        self.start_time = ''
        self.end_time = ':'.join(DateGo.now_ymd())

        self.params = {
            'searchtype': '1',
            'page_index':'1',
            'bidSort': '0',
            'pinMu': '0',
            'bidType': str(self.bidType),
            'displayZone':'',
            'zoneId':'',
            'kw':self.keyword,
            'start_time':self.start_time,
            'end_time':self.end_time,
            'timeType': '3'
        }
        self.headers = {
            'Cookie': 'JSESSIONID=EgPd86-6id_etA2QDV31Kks3FrNs-4gwHMoSmEZvnEktWIakHbV3!354619916; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; td_cookie=2144571454; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1545611064,1545618402,1545618414; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1545618495',
            'Host': 'search.ccgp.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.8 Safari/537.36',
            'keep-alive':'False'
        }

    def get_page(self,page_index):
        try:
            self.params['page_index'] = page_index
            response = requests.get(url=self.url,headers=self.headers,params=self.params)
            if response.status_code == 200:
                html = response.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
                return html
            else:
                print(response.status_code)
        except requests.ConnectionError:
            return None

    def get_detail_page(self,url):
        try:
            response = requests.get(url=url,timeout=5)
            if response.status_code == 200:
                html = response.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
                return html
        except requests.ConnectionError:
            return None


    def get_all_url(self,html):
        pattern1 = '<.*?(href=".*?htm").*?'
        href_url = re.findall(pattern1, html, re.I)
        url_list = []
        for url in href_url:
            url1 = url.replace('href=','').replace('"','')
            url_list.append(url1)
        return url_list


    def parse_datail_page(self,html,url):
        table_list = html.xpath('//div[@class="table"]//tr')

        if self.keyword == '医疗' or '卫生':
            label = '医疗卫生'
        elif self.keyword == '工程' or '建设':
            label = '工程建设'
        elif self.keyword == '环保' or '绿化':
            label = '环保绿化'
        elif self.keyword == '信息':
            label = '信息建设'
        elif self.keyword == '办公':
            label = '办公文教'
        elif self.keyword == '商业服务':
            label = '商业服务'
        else:
            label = None

        if self.bidType == 1:
            pStatus = '招标'
        elif self.bidType == 7:
            pStatus = '中标'
        elif self.bidType == 5:
            pStatus = '资审'
        elif self.bidType == 12:
            pStatus = '流标'
        else:
            pStatus = '其他'

        all_info = {
            'url':None,
            '采购项目名称':None,
            '爬取时间':None,
            '基建业分类':label,
            '项目状态':pStatus,
            '采购单位':None,
            '行政区域':None,
            '公告时间':None,
            '招标文件售价': None,
            #'获取招标文件时间':None,
            #'获取招标文件地点': None,
            #'开标时间':None,
            #'开标地点':None,
            '预算金额':None,
            '项目联系人':None,
            '项目联系电话':None,
            '采购单位地址':None,
            '采购单位联系方式':None,
            '代理机构名称':None,
            '代理机构地址': None,
            '代理机构联系方式':None
        }
        all_info['url']=url
        try:
            for table in table_list:
                if len(table.xpath('td[@class="title"]/text()'))>0:
                    title = ''.join(table.xpath('td[@class="title"]/text()'))
                    value = ''.join(table.xpath('td[@colspan="3"]/text()'))
                    print(title,value)
                    if title == '品目':
                        continue

                    if (title.find('附件')==0):
                        value = 'http://www.ccgp.gov.cn/oss/download?uuid='+''.join(table.xpath('td[@colspan="3"]/a/@id'))
                    if ('公告时间' in title):
                        title = '公告时间'
                        value = table.xpath('td[@width="168"]/text()')[1]
                        district_key = '行政区域'
                        district_value = (table.xpath('td[@width="168"]/text()'))[0]
                        all_info[district_key]=district_value
                    if '首次公告日期' in title :
                        title = '首次公告日期'
                        value = table.xpath('td[@width="168"]/text()')[0]
                        key='更正日期'
                        zhongbiaoriqi_value = table.xpath('td[@width="168"]/text()')[1]
                        all_info[key]=zhongbiaoriqi_value
                    if '本项目招标公告日期中标日期' in title :
                        title = '本项目招标公告日期'
                        value = table.xpath('td[@width="168"]/text()')[0]
                        zhongbiaoriqi_key = '中标日期'
                        zhongbiaoriqi_value = table.xpath('td[@width="168"]/text()')[1]
                        all_info[zhongbiaoriqi_key]=zhongbiaoriqi_value
                    if '本项目招标公告日期成交日期' in title:
                        title = '本项目招标公告日期'
                        value = table.xpath('td[@width="168"]/text()')[0]
                        zhongbiaoriqi_key = '中标日期'
                        zhongbiaoriqi_value = ''.join(table.xpath('td[@width="168"]/text()'))[11:]
                        all_info[zhongbiaoriqi_key] = zhongbiaoriqi_value
                    all_info[title] = value
                    all_info['爬取时间']= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        except:
            return False
        else:
            return all_info


    def start_getInfo(self,url):
        html = self.get_detail_page(url)
        html = etree.HTML(html)
        all_info = self.parse_datail_page(html,url)
        print(all_info)



if __name__ == '__main__':
    kw_list = ['医疗','卫生','工程','建设','环保','绿化','信息','办公','商业服务']
    bidType_list = [7,1,5,12]
    # bidType:  1 -> 招标 、7 -> 中标 、5 -> 资审 、12-> 流标
    for kw in kw_list:
        for bid in bidType_list:
            zhenfucaigouSpider = ZhenfucaigouSpider(keyword=kw,bidType=bid)
            for i in range(1,2):
                print('正在爬取第{}页'.format(str(i)))
                html = zhenfucaigouSpider.get_page(page_index=i)
                url_list =zhenfucaigouSpider.get_all_url(html)
                threads=[]
                for url in url_list:
                   threads.append(threading.Thread(target=zhenfucaigouSpider.start_getInfo,args=(url,)))
                for i in range(len(url_list)):
                    threads[i].start()
                for i in range(len(url_list)):
                    threads[i].join()
                time.sleep(5)
            time.sleep(5)
        time.sleep(5)