# -*- coding: utf-8 -*-
# @Time    : 2021/10/25 13:41
# @IDE ：PyCharm

import requests

url = 'https://fanyi.so.com/index/search?eng=1&validate=&ignore_trans=0&query=trans'
headers = {
'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'no-cache',
'Connection': 'keep-alive',
'Content-Length': '0',
'Host': 'fanyi.so.com',
'Origin': 'https://fanyi.so.com',
'Pragma': 'no-cache',
'pro': 'fanyi',
'Referer': 'https://fanyi.so.com/?src=onebox',
'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
}
# 长度有限
text = '''829年英国政府颁布天主教徒解放法，取消对爱尔兰天主教徒的歧视性政策。随着爱尔兰自治运动的开展，爱尔兰的新教徒担心爱尔兰的自治或独立将使他们成为一个天主教占多数的国家中的少数群体，因而成立联合派，主张爱尔兰继续留在联合王国之内。
20世纪初，随着爱尔兰自治运动的日益强大，新芬党副领袖米歇尔·奥尼尔（Michelle O’Neil）出任副首席部长，北爱地方政府恢复运作。'''
data = {
    'eng': '1',
    'validate':'',
    'ignore_trans': '0',
    'query': text
}
d = requests.post(url,headers=headers,data=data).json()
print(d['data']['fanyi'])