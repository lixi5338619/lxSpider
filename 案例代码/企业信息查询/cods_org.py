#coding=utf-8

import requests
from fontTools.ttLib import TTFont
import re
from urllib import parse
import hashlib
import threading

'''     cods.org.cn
《统一社会信用代码公示查询平台》
        微信小程序版
'''

def requests_data(data):
    jsonString = parse.quote(data)
    sign = hashlib.md5((jsonString+'A523B4A5C52203AA9C2D97F6CB45CB35').encode(encoding='UTF-8')).hexdigest()
    seek_data = {
        'jsonString': jsonString,
        'sign': sign
    }
    return seek_data


def seek(keyword):
    seek_url = 'https://ss.cods.org.cn/MiniProService/search/searchRMini'
    message_url = 'https://ss.cods.org.cn/MiniProService/detailPage/detail.base'
    history_url = 'https://ss.cods.org.cn/MiniProService/detailPage/findHistoryInfo'
    data = '{"q":"%s","t":"common",' \
                   '"currentPage":1,"xzqh":"",' \
                   '"jglx":"","zczj":"",' \
                   '"clrq":"","mobile":"",' \
                   '"isDeepSearch":false,' \
                   '"platform":"weixin",' \
                   '"openid":"o0VVO5XEoYaP_redhLOIiv5yCjFE"}' % keyword
    seek_data = requests_data(data)
    se = requests.post(url=seek_url, data=seek_data).text
    encjgdm = re.findall(r'"encJgdm":"(.*?)"',se)[0]
    threads1 = [threading.Thread(target=message,args=(encjgdm,keyword,message_url,)),
                threading.Thread(target=message,args=(encjgdm,keyword,history_url,))]
    for t1 in threads1:
        t1.start()
    for t2 in threads1:
        t2.join()


def message(encjgdm,keyword,url):
    data = '{"jgdm":"%s","keyword":"%s",' \
           '"platform":"weixin","openid"' \
           ':"o0VVO5XEoYaP_redhLOIiv5yCjFE"}'%(encjgdm,keyword)
    seek_data = requests_data(data)
    se = requests.post(url, data=seek_data).text
    textt(se)


def textt(text):
    global te
    te = te+text+'\r\n'
    return te


def unicod(unis):
    font = TTFont('D:/Chrome_Downloads/SourceHanSansCN-Normal-2500.woff')  # 打开本地的ttf文件
    bestcmap = font['cmap'].getBestCmap()
    print(bestcmap)
    best1 = {}
    best2 = {}
    best3 = {}
    for key in bestcmap:
        if key >= 19968:
            best2[key]=bestcmap[key].replace('uni','\\u').lower()
        else:
            best1[key] = bestcmap[key].replace('uni','\\u').lower()
    pr1=list(best1)
    pr2=list(best2)
    i=0
    for prs in pr1:
        best3[best1[prs]]=best2[pr2[i]]
        i+=1
    uni = ''
    for ii in unis:
        res = ii.encode("unicode_escape").decode()
        try:
            uni+=best3[res].encode('utf-8').decode('unicode_escape')
        except:
            uni+=res.encode('utf-8').decode('unicode_escape')
    return uni


def pssaw(woff):
    url = 'https://ss.cods.org.cn/css/woff/%s.woff2'%woff
    r = requests.get(url)
    with open("fonts.woff2", "wb") as code:
        code.write(r.content)
    dic = {}
    wei = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    font = TTFont('fonts.woff2')
    bestcmap = font['cmap'].getBestCmap()
    key_list = list(bestcmap)
    dic_key = bestcmap[key_list[36]]
    dic_3_7 = int(dic_key[3:-1])
    dic_un = dic_key[-1].lower()
    list_wei = wei.index(dic_un)
    y = 0
    y_count = 0
    a_z = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    o_9_a_z = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] + a_z
    while y < 3:
        for we in wei:
            if list_wei > 15:
                dic_3_7 += 1
                list_wei = list_wei - 16
            dic['\\u' + str(dic_3_7) + wei[list_wei]] = o_9_a_z[y_count]
            if y_count >= 35:
                break
            y_count += 1
            list_wei += 1
        y += 1
    return dic


def requests_url(url):
    header = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'kefuCookie=bd3cfa94a81c4c60a7555d1729ceebdf; _ga=GA1.3.1342218955.1613999997; __utma=48894260.1342218955.1613999997.1614301331.1614400327.6; __utmc=48894260; __utmz=48894260.1614400327.6.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; _gid=GA1.3.1472481659.1614400327; Hm_lvt_f4e96f98fa73da7d450a46f37fffbf56=1613999997,1614239520,1614239991,1614400327; __utmb=48894260.3.10.1614400327; Hm_lpvt_f4e96f98fa73da7d450a46f37fffbf56=1614400351; JSESSIONID=32C0D9C9459310B0C739D6120BE07CFA; userCookie=a52bdccc-e030-45ad-2b11-f8cd03e564bf; key=%5B%7B%22title%22%3A%22yinshan%22%2C%20%22link%22%3A%22wx_searchPro.action%3Fkeyword%3Dyinshan%22%2C%20%22other%22%3A%22%22%7D%2C%7B%22title%22%3A%22%E7%BF%81%E4%B8%80%22%2C%20%22link%22%3A%22wx_searchPro.action%3Fkeyword%3D%E7%BF%81%E4%B8%80%22%2C%20%22other%22%3A%22%22%7D%2C%7B%22title%22%3A%22%E3%B6%A8%E4%B8%80%22%2C%20%22link%22%3A%22wx_searchPro.action%3Fkeyword%3D%E3%B6%A8%E4%B8%80%22%2C%20%22other%22%3A%22%22%7D%2C%7B%22title%22%3A%22%E4%B8%8A%E6%98%AF%22%2C%20%22link%22%3A%22wx_searchPro.action%3Fkeyword%3D%E4%B8%8A%E6%98%AF%22%2C%20%22other%22%3A%22%22%7D%2C%7B%22title%22%3A%22%E4%B8%80%E4%BA%8C%22%2C%20%22link%22%3A%22wx_searchPro.action%3Fkeyword%3D%E4%B8%80%E4%BA%8C%22%2C%20%22other%22%3A%22%22%7D%2C%7B%22title%22%3A%22%C3%A4%C2%B8%C2%AD%C3%A5%C2%9B%C2%BD%C3%A7%C2%A7%C2%BB%C3%A5%C2%8A%C2%A8%22%2C%20%22link%22%3A%22wx_searchPro.action%3Fkeyword%3D%C3%A4%C2%B8%C2%AD%C3%A5%C2%9B%C2%BD%C3%A7%C2%A7%C2%BB%C3%A5%C2%8A%C2%A8%22%2C%20%22other%22%3A%22%22%7D%2C%7B%22title%22%3A%22%E9%9A%90%E5%B1%B1%E7%A7%91%E6%8A%80%22%2C%20%22link%22%3A%22wx_searchPro.action%3Fkeyword%3D%E9%9A%90%E5%B1%B1%E7%A7%91%E6%8A%80%22%2C%20%22other%22%3A%22%22%7D%2C%7B%22title%22%3A%22%E9%BB%91%E9%BE%99%E6%B1%9F%E5%8D%8E%E6%9D%A5%E5%9F%8E%E5%B8%82%E5%BB%BA%E8%AE%BE%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%20%22link%22%3A%22wx_searchPro.action%3Fkeyword%3D%E9%BB%91%E9%BE%99%E6%B1%9F%E5%8D%8E%E6%9D%A5%E5%9F%8E%E5%B8%82%E5%BB%BA%E8%AE%BE%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%20%22other%22%3A%22%22%7D%5D'
    }
    se = requests.get(url,headers=header).text
    woff = re.findall(r"src:url\('/css/woff/(.*?)\.woff2",se)[0]
    dic = pssaw(woff,)
    html1 = ''
    for ses in se:
        res = ses.encode("unicode_escape").decode()
        try:
            html1+=dic[res]
        except:
            html1+=ses
    return unicod(html1)


if __name__ == '__main__':
    te = ''
    keyword = '今日头条'
    sek = seek(keyword)
    print(te)
