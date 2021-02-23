# -*- coding: utf-8 -*-
# @Author  : lx
# @IDE ：PyCharm


# 国家电网招标采购网

sgcc = 'https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/noteList'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Host': 'ecp.sgcc.com.cn',
    'Origin': 'https://ecp.sgcc.com.cn',
    'Referer': 'https://ecp.sgcc.com.cn/ecp2.0/portal/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}
import requests
data = {"index":2,"size":20,"firstPageMenuId":"20180502001","orgId":"","key":"","year":""}
print(requests.post(url=sgcc, headers=headers, json=data).text)



detail_url = 'https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/getNoticeWin'
dataId = '2021022260391497'
#print(requests.post(url=detail_url, headers=headers, json=dataId).text)
