# -*- coding: utf-8 -*-
# @Time    : 2021/2/24 14:34
# @Author  : lx
# @IDE ：PyCharm

# 推荐
import requests,time,json
from urllib.parse import urlencode

# FIXME 必须修改 authorization，对小程序抓包可得
headers_login = {'accept': '*/*',
                'accept-type': 'application/json',
                'authorization': '修改修改',
                'device-fingerprint':'WHJMrwNw1k/EDrs4qQu7qho7mmYuri0YzaIx1p+ZruHXU5ABFod6r13el9Gk7wXXC5zMfJLxaBMpubNTyqfbLczzvrRRHlcJkdCW1tldyDzmauSxIJm5Txg==1487582755342',
                'accept-encoding': 'br, gzip, deflate',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
                'accept-language': 'zh-cn'
                }


# 推荐笔记
def note_feed():
    url = 'https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/homefeed/personalNotes?category=homefeed_recommend&cursorScore=&geo=&page=1&pageSize=20&needGifCover=true'
    headers_login.update({'x-sign': 'X5499d155d5267fd1c53418f0cab1624d'})
    response = requests.get(url=url, headers=headers_login).text
    print(response)


# 笔记评论
def note_comment():
    url = 'https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/notes/60350688000000002103bb03/comments?pageSize=10'
    headers_login.update({'x-sign': 'Xa56ea88af4cae1970a6e6a3986bddab3'})
    response = requests.get(url=url, headers=headers_login).text
    print(response)


# 搜索笔记
def search_note(keyword,page=1):
    url = f'https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/search/notes?keyword={keyword}&sortBy=general&page={page}&pageSize=20&prependNoteIds=&needGifCover=true'
    response = requests.get(url=url, headers=headers_login).text
    print(response)
#search_note(keyword='春季穿搭')


# 搜索商品
def search_goods(keyword,page=1):
    url = f'https://www.xiaohongshu.com/api/store/ps/products?keyword={keyword}&page={page}&per_page=20'
    response = requests.get(url=url, headers=headers_login).text
    print(response)
#search_goods(keyword='春季穿搭')


# 搜索用户
def search_users(keyword,page=1):
    # 现在也需要x-sign
    url = f'https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/search/users?keyword={keyword}&page={page}&pageSize=20'
    response = requests.get(url=url, headers=headers_login).text
    print(response)
#search_users(keyword='春季穿搭')


# 商品评论
def goods_comments(goods_id, page=0):
    url = 'https://www.xiaohongshu.com/api/store/review/{}/product_review?'.format(goods_id)
    params = {'page': page,'erPage': '10','tab': '2',}
    headers = {'accept': 'application/json, text/plain, */*',
               'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI 5 MIUI/V8.1.6.0.MAACNDI) '
                             'Resolution/1080*1920 Version/6.8.0.3 Build/6080103 Device/(Xiaomi;MI 5) NetType/WiFi',
               'netapm': 'true',
               'Host': 'www.xiaohongshu.com',
               'Connection': 'Keep-Alive',
               'Accept-Encoding': 'gzip'
               }
    response = json.loads(requests.get(url=url+urlencode(params), headers=headers).text)['data']['reviews']
    if not response:
        return False
    for item in response:
        print({'评论时间': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['createTime'])),
               '评论': item['text'],
               '评论回复': item['descendants'][0]['text'] if item['descendants'] else '',
               '评论回复时间': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['descendants'][0]['createTime'])) if item['descendants'] else '',
               '评论图片url': item['images'][0] if item['images'] else '',
               '用户ID': item['userInfo']['userId'],
               '用户头像': item['userInfo']['userIcon'],
               '用户名字': item['userInfo']['userName'],
           '购买信息': item['variants'][0] if item['variants'] else ''})

#goods_comments('5c823e985305650461527e4f')
