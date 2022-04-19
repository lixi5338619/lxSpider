# -*- coding: utf-8 -*-
# @Time : 2022/1/13 16:48
# @auth : lx

import execjs
import requests
from lxpy import copy_headers_dict
sess = requests.session()

headers = copy_headers_dict('''
    origin: https://www.qimai.cn
    pragma: no-cache
    referer: https://www.qimai.cn/
    sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    sec-fetch-dest: empty
    sec-fetch-mode: cors
    sec-fetch-site: same-site
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36
''')

with open('get_analysis.js','r',encoding='utf-8') as f:
    jscode = f.read()

js = execjs.compile(jscode)
analysis = js.call('get_analysis', "/rank/index","free")

req = sess.get(url="https://api.qimai.cn"+analysis['url'],params=analysis['params'], headers=headers)

print(req.url)
print(req.text)