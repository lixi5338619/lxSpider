# -*- coding: utf-8 -*-
# @Time    : 2019/7/29 上午11:36
# @Author  : lx

import scrapy
import json
import re
import time
from lxpy import DateGo     # pip install lxpy

'''
scrapy-spider 文件
热搜榜 + 热搜对应的话题数据
'''

class WeiboSearchSpider(scrapy.Spider):
    start_urls = [
        'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type%3Drealtimehot%26mi_cid%3D100103%26pos%3D0_0%26c_type%3D30%26display_time%3D1564024581&luicode=10000011&lfid=231583&featurecode=10000326'
              ]

    def yi_wan_change_tools(self,obj):
        obj = str(obj)
        if obj[-1] == '亿':
            obj = float(obj[:-1]) * 10 * 10 * 1000000
        elif obj[-2:] == '千万':
            obj = float(obj[:-2]) * 10 * 10 * 100 * 1000
        elif obj[-1] == '万':
            obj = float(obj[:-1]) * 10 * 10 * 100
        elif obj[-1] == '-':
            return obj
        return int(obj)


    def wan_jia_change_tools(self,obj):
        obj = str(obj)
        if obj[-2:] == '亿+':
            obj = float(obj[:-2]) * 10 * 10 * 1000000
        elif obj[-2:] == '万+':
            obj = float(obj[:-2]) * 10 * 10 * 100
        elif obj[-3:] == '千万+':
            obj = float(obj[:-3]) * 10 * 10 * 100 * 1000
        return int(obj)


    def parse(self, response):
        #TODO 热搜榜
        if  'containerid=106003' in str(response.url):
            json_text = json.loads(response.text)
            card_group = json_text['data']['cards'][0]['card_group']
            if len(card_group) >50:
                card_group = card_group[len(card_group)-50:]    # 第一个不要
            search_hot_item = {}                                # search_hot_item 热搜榜map
            search_hot_item['catchTime'] = DateGo.now_data()
            dict_1 = {}
            dict_2 = {}
            for card in card_group:
                rank = re.findall('img_search_(.*?)\.png', card['pic'])
                if rank:
                    rank = int(rank[0])
                else:
                    rank = -1
                search_hot_item['keywordTop'] = card['desc']
                dict_1[card['desc']] = rank
                dict_2[card['desc']] = int(card['desc_extr'])

            search_hot_item['keywordTop'] = dict_1
            search_hot_item['keywordNum'] = dict_2

            # TODO 热搜榜- search_hot_item

            for url_desc in card_group:
                for page in range(1,2):     # 页数
                    topic_hot_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D%23{}%23%26t%3D0&isnewpage=1&luicode=10000011&lfid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&page_type=searchall&page={}'.format(url_desc['desc'],page)
                    yield scrapy.Request(url=topic_hot_url,callback=self.wbTopic)


    def wbTopic(self,response):
        topic_hot_dic = {}                                  # topic_hot_dic 热搜话题榜map
        topic = dict()
        json_text = json.loads(response.text)
        cardlist_head_cards = json_text['data']
        if not cardlist_head_cards['cards']:
            print('话题请求异常，重新请求')
            time.sleep(1.5)
            yield scrapy.Request(url=response.url,callback=self.wbTopic,
                                 dont_filter=False)
            return

        cardlist_head_cards = cardlist_head_cards['cardlistInfo']
        cardlist_head_cards = cardlist_head_cards['cardlist_head_cards']
        title = cardlist_head_cards[0]['head_data']['title']
        read = cardlist_head_cards[0]['head_data']['midtext']
        topPic = cardlist_head_cards[0]['head_data']['portrait_url']
        if read:
            yuedu = re.findall('阅读(.*?) ', read)[0]
            taolun = re.findall('讨论(.*)  详情>', read)[0]
            topic['readNum'] = self.yi_wan_change_tools(yuedu)            # 话题阅读量
            topic['discussNum'] = self.yi_wan_change_tools(taolun)        # 话题讨论量

        topic['topPic'] = topPic                                     # 话题封面图
        topic['programId'] = None                                    # 未定 ！
        topic['title'] = title                                       # 话题名字，带#号
        topic['catchTime'] = DateGo.now_data()                       # 话题时间
        topic['profile'] = json_text['data']['cardlistInfo']['desc'] # 话题导语/简介
        card_list = json_text['data']['cards']
        topic['articles'] = []

        for card in card_list:
            s = {}
            '''用户发布的话题文章'''
            s['mid'] = card['mblog']['id']                                    # 文章id
            s['publishTime'] = DateGo.weibo_date(card['mblog']['created_at']) # 时间
            if len(s['publishTime'])==5:
                s['publishTime'] = str(DateGo.now_ymd()[0])+'-'+s['publishTime']+' 00:00:00'
            if len(s['publishTime']) == 10:
                s['publishTime'] = str(s['publishTime']) + ' 00:00:00'
            s['forwardNum'] = card['mblog']['reposts_count']                  # 转发
            s['commentNum'] = card['mblog']['comments_count']                 # 评论
            s['likeNum'] = card['mblog']['attitudes_count']                   # 点赞
            s['forwardNum'] = self.wan_jia_change_tools(s['forwardNum'])
            s['commentNum'] = self.wan_jia_change_tools(s['commentNum'])
            s['likeNum'] = self.wan_jia_change_tools(s['likeNum'])
            s['content'] = card['mblog']['text']                              # 内容
            s['content_url'] = card['scheme']                                 # 文章详情链接

            '''发布话题文章的用户'''
            user = card['mblog']['user']
            s['authorId'] = user['id']                                        # 用户id
            s['authorPic'] = user['profile_image_url']                        # 用户头像
            s['authorName'] = user['screen_name']                             # 用户名称
            s['fansNnm'] = user['followers_count']                            # 粉丝数

            s['followNum'] = user['follow_count']                             # 关注数
            s['weiboNum'] = user['statuses_count']                            # 微博数
            s['verified_reason'] = user.get('verified_reason',-1)           # 认证信息


            '''用户发布的图片'''
            s['articlePic'] = []
            try:
                card_pics = card['mblog']['pics']
                if len(card_pics) > 0:
                    for i in range(len(card_pics)):
                        img = card['mblog']['pics'][i]['url']
                        s['articlePic'].append(img)
            except:
                s['articlePic'] = []

            '''用户发布的视频'''
            if '微博视频' in card['mblog']['text'][-30:]:
                page_info = card['mblog']['page_info']
                page_pic = page_info['page_pic']['url']                     # 视频背景图
                s['articlePic'].append(page_pic)
                try:
                    s['video_info'] = page_info['content2']               # 视频信息
                except:
                    s['video_info'] = None
                s['video_type'] = page_info['type']                       # video
                s['video_count'] = page_info.get('play_count',-1)         # 播放次数
                s['video_url'] = page_info['media_info']['stream_url']    # 视频链接->微博的具有时效性。
            if s['articlePic'] == []:
                s['articlePic'] = None

            topic['articles'].append(s)              # 将用户话题内容添加到内容articles列表中

        topic_hot_dic['wbTopic'] = topic             # 将话题添加到wbTopicList话题列表中
        print(topic_hot_dic)

