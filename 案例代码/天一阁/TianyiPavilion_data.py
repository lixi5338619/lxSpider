import requests,json
from lxpy import copy_headers_dict
import execjs

def get_token():
    js = execjs.compile('''
    var CryptoJS = require("crypto-js");
    function token() {
        var e = e = "G3HT5CX8FTG5GWGUUJX8B5SWJTXS1KRC";
        var t = (Math.random() + "").substr(-6, 6) + +new Date;
        return CryptoJS.AES.encrypt(t, CryptoJS.enc.Utf8.parse(e), {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        }).toString()
    }
''')
    return js.call('token')


def outside_response():
    headers = copy_headers_dict('''
        Accept: application/json, text/plain, */*
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7
        appId: 4f65a2a8247f400c8c29474bf707d680
        Cache-Control: no-cache
        Connection: keep-alive
        Content-Type: application/json;charset=UTF-8
        Cookie: UM_distinctid=1820ef46444183-007501eeb5882-26021a51-1fa400-1820ef46445204; CNZZDATA1281082432=1218754449-1658105833-%7C1658128765
        Host: www.tianyige.com.cn:8008
        Origin: http://www.tianyige.com.cn:8008
        Pragma: no-cache
        Referer: http://www.tianyige.com.cn:8008/SearchPage?title=1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
    ''')
    headers.update({'token':get_token()})
    data = {"param":{"pageNum":1,"pageSize":6,"isAdminQuery":False,"type":0}}
    kw = '1'
    url =f'http://www.tianyige.com.cn:8008/g/sw-anb/api/queryCatalogBySort?classCode=&title={kw}'
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)


outside_response()