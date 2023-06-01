"""
荔枝网搜索关键词
"""
import time
import hashlib
import requests
import json
import hmac
import base64
import execjs


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def get_sign(data):
    js = '''
        const md5 = require("crypto-js/md5");
        const hmac_sha256 = require("crypto-js/hmac-sha256");
        const base64 = require("crypto-js/enc-base64");
        const CryptoJS = require("crypto-js");
        function get_signature(payload) {
            return CryptoJS.enc.Base64.stringify(md5(payload));
        }
    '''
    ctx = execjs.compile(js)
    funcName = """get_signature('{}')""".format(data)
    pwd = ctx.eval(funcName)
    return pwd


def get_signature(data):
    method = 'POST'
    target_url = 'https://gdtv-api.gdtv.cn/api/search/v1/news'
    ts_ms = int(time.time()*1000)
    data_sign = get_sign(data)
    message_text = '\n'.join([method, target_url, str(ts_ms), data_sign])
    CONST_KEY = 'dfkcY1c3sfuw0Cii9DWjOUO3iQy2hqlDxyvDXd1oVMxwYAJSgeB6phO8eW1dfuwX'
    hmac_obj = hmac.new(key=CONST_KEY.encode(), msg=message_text.encode(), digestmod=hashlib.sha256)
    signature = base64.b64encode(hmac_obj.digest()).decode()
    return ts_ms, signature


def run():
    formdata = '{"keyword":"青岛","pageNum":1,"type":-1,"pageSize":20}'
    timestamp, signature = get_signature(formdata)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'x-itouchtv-ca-key': '89541443007807288657755311869534',
        'x-itouchtv-ca-signature': signature,
        'x-itouchtv-ca-timestamp': str(timestamp),
        'x-itouchtv-client': 'WEB_PC',
        'x-itouchtv-device-id': 'WEB_3ee50450-f38c-11ec-914c-f7b7f9f4989b',
        'content-type': 'application/json',
    }
    resp = requests.post('https://gdtv-api.gdtv.cn/api/search/v1/news', data=formdata.encode('utf-8'), headers=headers).json()
    for index, i in enumerate(resp['newsItems']['list']):
        print(index, i['title'])


run()

