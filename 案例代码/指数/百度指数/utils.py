import queue
import math
import datetime
import random
import time
import json

import requests


headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}


def get_time_range_list(startdate, enddate):
    """
        切分时间段
    """
    date_range_list = []
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    while 1:
        tempdate = startdate + datetime.timedelta(days=300)
        if tempdate > enddate:
            date_range_list.append((startdate, enddate))
            break
        date_range_list.append((startdate, tempdate))
        startdate = tempdate + datetime.timedelta(days=1)
    return date_range_list


def split_keywords(keywords: list) -> [list]:
    """
    一个请求最多传入5个关键词, 所以需要对关键词进行切分
    """
    return [keywords[i*5: (i+1)*5] for i in range(math.ceil(len(keywords)/5))]


def get_params_queue(start_date, end_date, keywords):
    """
        获取参数队列
    """
    params_queue = queue.Queue()
    keywords_list = split_keywords(keywords)
    time_range_list = get_time_range_list(start_date, end_date)
    for start_date, end_date in time_range_list:
        for keywords in keywords_list:
            params = {
                'keywords': keywords,
                'start_date': start_date,
                'end_date': end_date
            }
            params_queue.put(params)
    return params_queue


def http_get(url, cookies):
    """
        发送get请求, 程序中所有的get都是调这个方法
        如果想使用多cookies抓取, 和请求重试功能
        在这自己添加
    """
    _headers = headers.copy()
    _headers['Cookie'] = cookies
    response = requests.get(url, headers=_headers, timeout=5)
    if response.status_code != 200:
        raise requests.Timeout
    return response.text


def get_key(uniqid, cookies):
    """
    """
    url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
    html = http_get(url, cookies)
    datas = json.loads(html)
    key = datas['data']
    return key


def decrypt_func(key, data):
    """
        数据解密方法
    """
    a = key
    i = data
    n = {}
    s = []
    for o in range(len(a)//2):
        n[a[o]] = a[len(a)//2 + o]
    for r in range(len(data)):
        s.append(n[i[r]])
    return ''.join(s).split(',')


def sleep_func():
    """
        sleep方法, 单账号抓取过快, 一段时间内请求会失败
    """
    sleep_time = random.choice(range(50, 90)) * 0.1
    time.sleep(sleep_time)


def test_cookies(cookies):
    """
        测试cookie是否可用
    """
    html = http_get('https://www.baidu.com/', cookies)
    return '退出' in html
