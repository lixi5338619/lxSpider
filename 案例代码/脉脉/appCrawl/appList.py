# -*- coding: utf-8 -*-
# @IDE ：PyCharm

import requests,time
from appCrawl.config import headers,JRlables,access_token

from db import DB
d = DB()




# 列表

def requestList(p,c,wt,pf,mj,access_token,o,lim):
    AppList = f'https://maimai.cn/search/uh_adsearch?w=&p={p}&c={c}&t=&cp=&curcp=&excp=&pos=&wt={wt}&sch=&pro=&m=&dist=&pf={pf}&mj={mj}&search_sid=c94687d7-6da3-4f63-b3e6-93f55def0b91&voyager_params_page=big_search&jsononly=1&u=233324840&access_token={access_token}&version=5.3.16&channel=Baidu&_csrf=q7ZGBypg-YpYjvGx6SJ5atahuwAUCN9jMF3I&_csrf_token=KA6YUVmn-k-4ebkgv-0jTHD5CmZbYPSTZlnI&o={o}&lim={lim}'
    dicts = requests.get(AppList,headers=headers).json()
    ucards = dicts['data']['adsearch']['ucards']
    for contact in ucards:
        item = {}
        item['search'] = {"pf": pf, "mj": mj, "p": p, "c": c}
        item['id'] = contact['id']
        item['name'] = contact['name']
        # item['py'] = contact['py']  # 名字拼音
        # item['avatar'] = contact['avatar']  # 头像
        # item['line1'] = contact['line1']  # 介绍
        # item['rank'] = contact['rank']  # 影响力
        # item['compos'] = contact['compos']  # 机构+职位
        # item['loc'] = contact['loc']  # 位置 -> 北京
        # item['gender'] = contact['gender']  # 性别
        # item['company'] = contact['company']  # 机构
        # item['position'] = contact['position']  # 职位
        # item['province'] = contact['province']  # 省 -> 北京
        # item['city'] = contact['city']  # 市 -> 海淀区
        item['url'] = 'https://maimai.cn/contact/detail/' + contact['encode_mmid']
        item['user_pfmj'] = {
                    "major1":contact['user_pfmj']['major1'],     # 所属行业标签 0218
                    "pf_name1":contact['user_pfmj']['pf_name1'], # 所属行业 -> 金融/互联网/政府
                    "mj_name1":contact['user_pfmj']['mj_name1'], # 所属岗位类型 -> CEO/创始人/公务员
                    }
        item['valid'] = 0

        d.insert_list(item)

    while 1:
        time.sleep(5)
        print(f"{p}{c},{pf},{mj}，Page:{o//600+1}")
        if len(ucards)==lim:
            o+=lim
            return requestList(p,c,wt,pf,mj,access_token,o,lim)
        elif len(ucards)<lim:
            print("没有下一页")
            print(AppList)
            break
        else:
            raise IndexError("ucards>lim")
    return




if __name__ == '__main__':
    #pf = '0201' # 行业标签
    #mj = ''  # 职业方向
    #wt = ''  # 工作时间  4：10年以上   3：5-10年  2：3-5年  1：1-3年 0：1年以内
    p = '北京'
    c = '东城区'  # 市区
    lim = 600  # 每页数量
    o = 0  # page 0 40 80 120
    for lable in JRlables:
        code = lable['code']
        pf,mj = code,''
        requestList(p=p,c=c,wt=None,pf=pf,mj=mj,access_token=access_token,o=o,lim=lim)
        time.sleep(1)
