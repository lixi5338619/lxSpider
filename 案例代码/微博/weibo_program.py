# -*- coding: utf-8 -*-
# @Time    : 2019/9/3 上午11:01
# @Author  : lx
# @Software: PyCharm

import scrapy
import json
from lxpy import DateGo  # pip install lxpy

'''微博综艺榜 剧集榜 影视榜'''

class WeiboBdSpiderSpider(scrapy.Spider):
    name = 'weibo_bdzyj'
    start_urls = []
    now_data = DateGo.now_data()
    headers_zy = {
                "User-Agent":"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
                'Host': 'rprank.tv.weibo.cn',
                'Referer': 'https://rprank.tv.weibo.cn/variety?cid=2_0_3_1566748800&immersiveScroll=150&topnavstyle=1',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'X-Requested-With': 'XMLHttpRequest',
                }

    yesterday_timec = DateGo.yesterday_timec()
    yesterday_date = DateGo.timec_change_dtime(yesterday_timec)

    zongyi_url = 'https://rprank.tv.weibo.cn/variety/aj/rank?page=1&status=2&bang=2&time={}&t=0'.format(yesterday_timec)
    juji_url = 'https://rprank.tv.weibo.cn/episode/aj/rank?page=1&status=2&bang=2&time={}&t=0'.format(yesterday_timec)
    movie_url = 'https://movie.weibo.com/movie/web/ajax_getRankTaobao?date=&data_type=movie_week_pollnew'
    url_list = []
    url_list.append(zongyi_url)
    url_list.append(juji_url)
    url_list.append(movie_url)


    headers_mv = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
        'Referer': 'https://movie.weibo.com/rank',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest',
                }


    def start_requests(self):
        for url in self.url_list:
            if 'movie.weibo.com' in url:
                yield scrapy.Request(url= url, callback=self.parse_movie, headers=self.headers_mv)
            else:
                yield scrapy.Request(url=url,callback=self.parse_zyjj,headers=self.headers_zy)


    '''解析微博影剧榜'''
    def parse_movie(self, response):
        doc = json.loads(response.text)
        dic = {}
        dic_list = []
        for item in doc['content']:
            q = {}
            q['name'] = item['name']
            q['film_id'] = item['film_id']
            q['directors'] = item['directors']
            q['actors'] = item['actors']
            q['keyword'] = item['keyword']
            q['weibo_id'] = item['weibo_id']
            q['poster'] = item['poster']
            q['release_time'] = item['release_time']
            q['sum'] = item['trendinfo']['sum']
            q['total_rank'] = item['trendinfo']['total_rank']
            dic_list.append(q)
        dic['dic_list'] = dic_list


    '''解析微博综艺和剧集榜'''
    def parse_zyjj(self, response):
        doc = json.loads(response.text)
        for doc_items in doc['data']['items']:
            item = {}
            item['publishTime'] = self.yesterday_date
            item['catchTime'] = self.now_data
            item['topRank'] = doc_items['rank']
