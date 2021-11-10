import requests
import os
import execjs

os.environ["EXECJS_RUNTIME"] = "Node"


def genSign(kw: str) -> dict:
    with open('./有道翻译.js', 'r') as rf:
        js = execjs.compile(rf.read())
        return js.call('r', kw)


def translator(kw,sess):
    url = "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Referer': 'https://fanyi.youdao.com/',
        #'Cookie': 'OUTFOX_SEARCH_USER_ID=-900337969@10.108.160.100; OUTFOX_SEARCH_USER_ID_NCOO=1443015609.972365; JSESSIONID=aaaJRD58ngQEJhLbL99Xx; ___rl__test__cookies=1634200940737'
    }

    data = genSign(kw)
    form_data = [
        ('i', kw),
        ('from', 'AUTO'),
        ('to', 'AUTO'),
        ('smartresult', 'dict'),
        ('client', 'fanyideskweb'),
        ('doctype', 'json'),
        ('version', 2.1),
        ('keyfrom', 'fanyi.web'),
        ('action', 'FY_BY_REALTlME'),
        ('salt', data['salt']),
        ('sign', data['sign']),
        ('lts', data['ts']),
        ('bv', data['bv'])
    ]
    res = sess.post(url=url, headers=headers, data=form_data)
    if '出错信息' in res.text:
        print("触发风控")
    else:
        print(res.text)


if __name__ == '__main__':
    # 访问频繁后会触发风控，只能换IP

    sess = requests.session()
    sess.get('https://fanyi.youdao.com/')
    while 1:
        translator(kw ='I get up in the morning and go running by the river',sess=sess)
        translator(kw ='我早上起床，去河边跑步',sess=sess)
        translator(kw ='我早上起床，去河边跑步 我早上起床，去河边跑步 我早上起床，去河边跑步我早上起床，去河边跑步',sess=sess)

