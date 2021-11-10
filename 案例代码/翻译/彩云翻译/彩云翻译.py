import requests
import json
import re
import base64

# 彩云翻译

html = requests.get('https://fanyi.caiyunapp.com/static/js/app.0396a6f01e89e3e0d836.js').text
token = re.findall('"token:(.*?)"',html,re.S)[0]
print(token)

sess = requests.session()
sess.headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'app-name': 'xy',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'device-id':'',
    'Host': 'api.interpreter.caiyunai.com',
    'Origin': 'https://fanyi.caiyunapp.com',
    'os-type': 'web',
    'os-version':'',
    'Pragma': 'no-cache',
    'Referer': 'https://fanyi.caiyunapp.com/',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'version': '1.8.0',
    'X-Authorization': f'token:{token}'
}

generate = 'https://api.interpreter.caiyunai.com/v1/user/jwt/generate'
browser_id = 'ec0ce103565e9928534549bdaede2301'
Authorization = sess.post(url=generate,data='{"browser_id": "%s"}'%browser_id).json()['jwt']

def caiyun(sentence,browser_id,Authorization):
    url = "https://api.interpreter.caiyunai.com/v1/translator"
    payload = {"source": sentence,
               "trans_type": "auto2en",
               "request_id": "web_fanyi",
               "media": "text",
               "os_type": "web",
               "dict": True,
               "cached": True,
               "replaced": True,
               "detect": True,
               "browser_id": browser_id
               }
    headers = {
        'content-type': "application/json",
        'T-Authorization': Authorization,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    sess.options(url)
    response = sess.post(url, data=json.dumps(payload), headers=headers)
    result = json.loads(response.text)
    return result

result = caiyun('godd',browser_id,Authorization)
print(result)

# result = base64.b64decode(result['target']).decode("utf-8")
# print(result)
