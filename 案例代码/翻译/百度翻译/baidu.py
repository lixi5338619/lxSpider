import requests
import os
import re 
from js2py import EvalJs

class BaiDuTS():
    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
             'Origin': 'https://fanyi.baidu.com',
            'Referer': 'https://fanyi.baidu.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.session = requests.Session()
        index_url = 'https://fanyi.baidu.com/'
        self.session.get(url=index_url, headers=self.headers)
        response_index = self.session.get(url=index_url,headers=self.headers)
        self.token = re.findall(r"token: '([0-9a-z]+)'", response_index.text)[0]
        self.gtk = re.findall(r'gtk = "(.*?)"', response_index.text)[0]
        with open(os.path.join('baidu.js'), 'r', encoding='utf-8') as f:
            baidu_js = f.read()
        self.ctx = EvalJs()
        self.ctx.execute(baidu_js)

    # 获取今天任意时刻的时间戳
    def today_anytime_tsp(self,hour, minute, second=0):
        from datetime import datetime, timedelta
        now = datetime.now()
        today_0 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        today_anytime = today_0 + timedelta(hours=hour, minutes=minute, seconds=second)
        tsp = today_anytime.timestamp()
        return str(int(tsp*1000))


    def translate(self,query):  
        sign=self.ctx.e(query,self.gtk)
        translate_url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
        acs_token=self.today_anytime_tsp(15,0,9)+ self.ctx.ascToken(translate_url)
        data = {
            'from':'en',
            'to': 'zh' ,
            'query': query,
            'transtype': 'realtime',
            'simple_means_flag': '3',
            'sign': sign,
            'token': self.token,
            'domain': 'common'
        }
        self.headers["Acs-Token"]=acs_token
        translate_api = 'https://fanyi.baidu.com/v2transapi'
        response = self.session.post(url=translate_api,headers=self.headers,data=data)
        result ='\n'.join([_['dst'] for _ in response.json()['trans_result']['data']])
        return result


f = BaiDuTS()
print(f.translate('and'))