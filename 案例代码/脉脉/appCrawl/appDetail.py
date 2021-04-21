# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 13:50
# @Author  : lx
# @IDE ：PyCharm

import requests
from appCrawl import config
from db import DB
from appCrawl.config import access_token
d = DB()

# 详情
def requestDetail(encode_mmid, access_token):
    AppDetail = f'https://maimai.cn/contact/basic/{encode_mmid}?access_token={access_token}&appid=3&channel=Baidu&fr=&from=webview%23%2Fsearch%2Fcontacts_all&is_node=1&job_dialog=&job_popup=&jsononly=1&only_recruiting=true&outofrel=false&page_type=big_search&position=&recid=&req_time=1618478938032&rn=1&screen_height=900&screen_width=1600&sid=5603c5c5-fa0a-494d-a58d-a6181795365d&u=233324840&version=5.3.16&webviewUserAgent=Mozilla%2F5.0%20%28Linux%3B%20Android%205.1.1%3B%20MI%209%20Build%2FNMF26X%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F74.0.3729.136%20Mobile%20Safari%2F537.36'
    data = requests.get(AppDetail, config.headers).json()
    return data


def parseDetail(dicts: dict, encode_mmid,item):
    data = dicts['data']
    contact = data['uinfo']
    cards = data['card']
    item['visitor_count'] = data['visitor_count']['cnt']  # 被看过
    item['article_count'] = data['articles']['count']  # 文章数
    item['jobs_count'] = data['jobs']['count']
    item['is_wiki'] = data['is_wiki']
    item['commercial_view_cnt'] = data['commercial_view_cnt']
    item['verify_time'] = data['verify_status']['identification_time']
    item['company_item'] = data['company']  # 机构信息
    item['work_exp'] = contact['work_exp']  # 工作经验
    item['education'] = contact['education']  # 教育经验
    item['xingzuo'] = contact.get('xingzuo')  # 星座
    item['id'] = contact['id']
    item['name'] = cards['name']  # 名字
    item['gender'] = cards['gender']  # 性别
    item['py'] = cards['py']  # 名字拼音
    item['avatar'] = cards['avatar']  # 头像
    item['line1'] = cards['line1']  # 介绍
    item['rank'] = cards['rank']  # 影响力
    item['compos'] = cards['compos']  # 机构+职位
    item['loc'] = cards['loc']  # 位置 -> 北京
    item['company'] = cards['company']  # 机构
    item['position'] = cards['position']  # 职位
    item['province'] = cards['province']  # 省 -> 北京
    item['city'] = cards['city']  # 市 -> 海淀区
    item['address'] = contact['address']  # 地址
    item['ht_province'] = contact.get('ht_province')  # 家乡省
    item['ht_city'] = contact.get('ht_city')  # 家乡市
    item['weibo_tags'] = contact['weibo_tags']  # weibo_tags
    item['headline'] = contact['headline']  # 简介提要
    item['url'] = 'https://maimai.cn/contact/detail/' + encode_mmid
    item['nomobile'],item['noemail'],item['noaccount']=None,None,None
    if contact['nomobile']!='仅好友可见' or contact['noemail']!='仅好友可见':
        item['nomobile'] = contact['nomobile']      # 电话
        item['noemail'] = contact['noemail']        # 邮箱
        item['noaccount'] = contact['noaccount']

    d.insert_Detail(item)
    d.update_list_valid(item['id'])
    print(item['name'],item['id'],item['compos'])

import time,random
if __name__ == '__main__':
    result = d.select_List()
    for li in result:
        item = {}
        item['url'] = li['url']
        item['search'] = li['search']
        item['user_pfmj'] = li['user_pfmj']
        encode_mmid = li['url'].split('https://maimai.cn/contact/detail/')[1]
        data = requestDetail(encode_mmid, access_token)
        parseDetail(dicts=data,encode_mmid=encode_mmid,item=item)
        time.sleep(random.randint(4,8))
