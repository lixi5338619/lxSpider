import requests
import execjs

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/octet-stream',
    'Cookie': 'JSESSIONID=AEEBD8C56042F7569EFA9F56D0F0E8C4',
    'Host': 'www.spolicy.com',
    'Origin': 'http://www.spolicy.com',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

def req_data(method,params):
    with open('spolicy.js','r',encoding='utf-8') as f:
        js = f.read()
    data = execjs.compile(js).call(method,params)
    data = ''.join([chr(i) for i in data['data']])
    return data

def req_list():
    data = req_data('req_list','4')
    resp = requests.post('http://www.spolicy.com/info_api/policyType/showPolicyType', data=data, headers=headers)
    print(resp.text)

def req_detail():
    data = req_data('req_detail','630c1f1468780907e889d2d4')
    resp = requests.post('http://www.spolicy.com/info_api/policyInfo/getPolicyInfo', data=data, headers=headers)
    print(resp.text)

def req_search():
    data = req_data('req_search','集成电路')
    resp = requests.post('http://www.spolicy.com/info_api/policyinfoSearchController/searchEsPolicyinfo', data=data, headers=headers)
    print(resp.text)


req_search()