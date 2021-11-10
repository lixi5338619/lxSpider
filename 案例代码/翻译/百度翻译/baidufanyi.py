# --*-- coding: utf-8 --*--

import re
import execjs
import requests

lang_url = 'https://fanyi.baidu.com/langdetect'
index_url = 'https://fanyi.baidu.com/?aldtype=16047'
translate_api = 'https://fanyi.baidu.com/v2transapi'
sess = requests.session()

sess.headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'fanyi.baidu.com',
    'Origin': 'https://fanyi.baidu.com',
    'Referer': 'https://fanyi.baidu.com/',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_token():
    while 1:
        response = sess.get(url=index_url).text
        print(sess.cookies)

        token = re.findall(r"token: '([0-9a-z]+)", response)
        if token:
            token = token[0]
            break
    return token


def get_sign(query):
    with open('baidu_encrypt.js', 'r', encoding='utf-8') as f:
        baidu_js = f.read()
    sign = execjs.compile(baidu_js).call('e', query)
    print(sign)
    return sign


def get_result(lang, query, sign, token):
    data = {
        'from': lang,
        'to': 'en',
        'query': query,
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'sign': sign,
        'token': token,
    }
    response = sess.post(url=translate_api,data=data)
    print(sess.cookies)

    result = response.json()

    if result.get('errmsg'):
        return '访问出现异常，请重试！'
    dst = result['trans_result']['data'][0]['dst']
    return dst


def trans(query):
    response = sess.post(url=lang_url,data={'query': query})
    try:
        lang = response.json()['lan']
    except:
        print(response.text)
        return
    token = get_token()
    sign = get_sign(query)
    result = get_result(lang, query, sign, token)
    print(result)


if __name__ == '__main__':
    # 百度请求频率高会异常，重试即可
    while 1:
        trans('我早上起床，去河边跑步')
        #trans('I get up in the morning and go running by the river')
