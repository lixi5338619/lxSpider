from lxpy import copy_headers_dict
import requests

headers = {
'user-agent':'Android511-AndroidPhone-10659-14-0-COMMENT-wifi',
'accept-encoding':'gzip, deflate',
'kg-rc':'1',
'kg-fake':'1887484938',
'kg-rf':'009888ce',
'x-router':'m.comment.service.kugou.com'
}


import time
clienttime = round(time.time())
dfid='10wxeO4AE9lK0Ek13L1LrvgC'
mid='304291870705239990160554795323375833919'
extdata='8616f71390c954c3f52bf53841fa4518'
uuid='cc133b26f7e7c93a89a4f7309002ddb2'
appid='1005'
schash='0930c43952c442a194129d20f48182fc'
code='fc4be23b4e972707f36b8a828a93ba8a'
clientver='10659'
mixsongid='274337675'
clienttoken='5841e1d4296732bd0015f52838bdae21bbfe0ded81d1960f0db7edae4d11f4fb'
ver='10'
kugouid='1887484938'
childrenid = '82117948'
p = '2'
pagesize = '20'
OIlwieks = '28dk2k092lksi2UIkp'

sign_params = f'OIlwieks{OIlwieks}appid={appid}childrenid={childrenid}clienttime={clienttime}clienttoken={clienttoken}clientver={clientver}code={code}dfid={dfid}extdata={extdata}kugouid={kugouid}mid={mid}mixsongid={mixsongid}p={p}pagesize={pagesize}uuid={uuid}ver={ver}OIlwieks{OIlwieks}'
import hashlib
m = hashlib.md5()
m.update(sign_params.encode(encoding='UTF-8'))
sign = m.hexdigest()
signature = '&signature='+sign
print(sign_params)
print(signature)
url = f'http://m.comment.service.kugou.com/r/v1/rank/newest?dfid={dfid}&mid={mid}&clienttime={clienttime}&extdata={extdata}&uuid={uuid}&appid=1005&schash={schash}&code={code}&clientver=10659&p=1&mixsongid={mixsongid}&clienttoken={clienttoken}&pagesize=20&ver=10&kugouid={kugouid}'
res = requests.post(url+signature,headers=headers)
print(res.url)
print(res.text)


