#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file: mafengwo
@time: 2021/2/3
@desc: 
"""
import execjs
import requests
import re

class MaFengWoSpider:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    }

    session = requests.session()
    session.headers = headers
    session.verify = False

    def start(self):
        response = self.session.get('http://www.mafengwo.cn/i/21452824.html').text
        js = re.search(r'document\.(.*?);location', response).group(1)
        ctx = execjs.compile(js)
        __jsl_clearance = ctx.eval('cookie').split(";")[0].split("=")[-1]
        self.session.cookies.update({
            "__jsl_clearance": __jsl_clearance
        })

        response = self.session.get('http://www.mafengwo.cn/i/21452824.html')
        js_obj = re.search(r';go\(([\s\S]*?)\)', response.text).group(1)
        js_obj = eval(js_obj)
        js_file_name = '{}.js'.format(js_obj['ha'])
        with open(js_file_name, "r") as f:
            js2 = f.read()
        ctx2 = execjs.compile(js2)
        __jsl_clearance = ctx2.call("go", js_obj) or ""
        self.session.cookies.update({
            "__jsl_clearance": __jsl_clearance.split("=")[1].split(";")[0]
        })
        response = self.session.get('http://www.mafengwo.cn/i/21452824.html')
        print(response.text)

if __name__ == '__main__':
    spider = MaFengWoSpider()
    spider.start()





