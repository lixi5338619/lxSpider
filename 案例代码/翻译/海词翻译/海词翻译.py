# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 14:50
# @IDE ：PyCharm

import requests
import time

d = time.time()*1000
register = f'http://capi.dict.cn/fanyi.php?_={d}'
sess = requests.session()
sess.headers = {
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Host': 'capi.dict.cn',
'Proxy-Connection': 'keep-alive',
'Referer': 'http://fanyi.dict.cn/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
}

appId = sess.get(register).text
kw = '''12, Time goes by so fast, people go in and out of your life. You must never miss the opportunity to tell these people how much they mean to you.
Time goes by so fast, people go in and out of your life. Don't miss the opportunity to tell them what they mean in your life.
I lied when I said I didn't like you. I lied when I said I didn't care. I lied when I told myself I'd never have feelings for you again.
14, One needs 3 things to be truly happy living in the world: some thing to do, some One to love, some thing to hope for.
One needs 3 things to be truly happy living in the world: some thing to do, some one to love, some thing to hope for.
15, No matter how bad your heart has been broken, The world doesn't stop for your grief. The sun comes right back up the next day.
No matter how bad your heart has been broken, the world doesn't stop for your grief. The sun still rises.
Accept what was and what is, and you'll have more positive energy to pursue what will be.
17, Until you make peace with who you are, you'll never be content with what you have.
Until you make peace with who you are, you'll never be content with what you have.
18, If you would hit the mark, You must aim a little above it. Every arrow that flies feels the attraction of earth. -Henry Wadsworth Longfellow
If you would hit the mark, you must aim a little above it. Every arrow that flies feels the attraction of earth. -Henry Wadsworth Longfellow.
19, If you wish to succeed, you should use persistence as your good friend, experience as your reference, prudence as your brother and hope as your sentry.
If you wish to succeed, you should use persistence as your good friend, experience as your reference, prudence as your brother and hope as your sentry.
20, I'll think of you every step of the way.'''
fr = 'en'
to = 'zh-CHS'
kw = ''.join(kw.split('\n'))
haici = f'http://api.microsofttranslator.com/V2/Ajax.svc/TranslateArray?from={fr}&to={to}&appId={appId}&texts=["{kw}"]'

while 1:
    print(requests.get(haici).text)
