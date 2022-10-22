import requests
import execjs

with open('同花顺.js','r') as f:
    js = f.read()
v = execjs.compile(js).call('v')
cookies = {'v': v}

headers = {} #自行添加

response = requests.get('http://basic.10jqka.com.cn/000001/company.html', headers=headers, cookies=cookies)