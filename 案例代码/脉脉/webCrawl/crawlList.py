# -*- coding: utf-8 -*-
# @Time    : 2021/4/13 15:21

# 脉脉网页版最多显示1599条数据。
# contacts_total: 1599 总数
# more : 1589 最大数量
# 先根据县区采集，如果数量超过1580则按百家姓检索


# 1秒请求1次列表页 被封

import requests,time
from db import DB
from appCrawl.config import access_token

url = 'https://maimai.cn/search/contacts?'
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "u=也需要修改下; access_token={};".format(access_token),
    "referer": "https://maimai.cn/web/search_center",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
}

def get_params(keyword,page):
    params = {
        "count": "20",
        "page": str(page),
        "query": keyword,
        "dist": "0",
        "searchTokens":"",
        "highlight": "true",
        "jsononly": "1",
        "pc": "1",
    }
    return params


f2 = open('data/error.txt', 'a+', encoding='utf-8')


List = [
     '察隅县', '天山区', '简阳县'
]

d = DB()
for keyword in List:
    page = 0
    ERO = False
    filterList = []
    while 1:
        if ERO:
            print("==================ERO 页码超过 ==================")
            break
        try:
            response = requests.get(url=url, params=get_params(keyword, page), headers=headers)
            data = response.json()
        except:
            print("ERROR:",keyword, page)
            break
        print(keyword,page)
        more = data['data']['more']
        contacts_total = data['data']['contacts_total']
        if more>1500:
            print(f"============ {keyword}:人数过多 >1500 ============")
            f2.write(keyword)
            f2.write('\n')
            break
        if page!=0 and more==0 or page>=contacts_total//10:
            print("================== total 页码超过 ==================")
            break
        contacts_total = data['data']['contacts_total'] # contacts_total

        for contacts in data['data']['contacts']:
            uid = contacts['uid']
            contact = contacts['contact']
            item = {}
            item['keyword'] = keyword
            item['id'] = contact['id']
            if item['id'] in filterList:
                print(response.url)
                ERO = True
                break
            else:
                filterList.append(item['id'])
            item['name'] = contact['name']
            item['py'] = contact['py']  # 名字拼音
            item['rank'] = contact['rank']  # 影响力
            item['avatar'] = contact['avatar']  # 头像
            item['line1'] = contact['line1']    # 介绍
            item['loc'] = contact['loc']  # 位置 -> 北京
            item['compos'] = contact['compos']  # 机构+职位
            item['gender'] = contact['gender']  # 性别
            item['company'] = contact['company']  # 机构
            item['position'] = contact['position']  # 职位
            item['province'] = contact['province']  # 省 -> 北京
            item['city'] = contact['city']  # 市 -> 海淀区
            item['url'] = 'https://maimai.cn/contact/detail/'+contact['encode_mmid']
            item['industry'] = contact['user_pfmj']['pf_name1'] # 所属行业 -> 金融/互联网/政府
            item['jobs'] = contact['user_pfmj']['pf_name1']     # 岗位类型 -> CEO/创始人/公务员
            item['login_time'] = contact['login_time']
            item['type_vip'] = contact['type_vip']
            item['valid'] = 0
            print(item['name'],item['compos'])
            d.insert_list(item)
        page+=1
        time.sleep(2.5)

f2.close()
d.close_spider()
