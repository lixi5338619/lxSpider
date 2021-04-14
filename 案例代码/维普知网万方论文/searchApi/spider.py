# -*- coding: utf-8 -*-

import requests
import time
import random
from lxml import etree
import re

'''获取随机UA'''
def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
    '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
    '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)
    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    userAgent = {"user-agent":ua}
    return userAgent


'''维普数据网'''
def get_weipu(keyword,searchtype='Content'):
    url = 'http://www.cqvip.com/data/main/search.aspx?'
    params = {
        'action': 'so',
        'tid': '0',
        'k': keyword,
        'curpage': '0',
        'perpage': '0',
        '_': str(time.time() * 1000),
        'rid': '0',
    }
    weipu_ua = get_ua().update({'X-Requested-With': 'XMLHttpRequest'})
    json_text = requests.get(url, headers=weipu_ua, params=params).json()
    recordcount = json_text['recordcount']

    item = {}
    item['success'] = json_text['success']
    item['recordcount'] = int(recordcount)
    if item['recordcount'] == 0:
        return item

    html = json_text['message']
    e = etree.HTML(html)
    item['articleList'] = []
    for li in e.xpath('//ul/li'):
        title = ''.join(li.xpath('.//tr[1]/th/a//text()'))          # 标题
        content_url = 'http://www.cqvip.com/'+''.join(li.xpath('.//tr[1]/th/a/@href'))
        sources = ''.join(li.xpath('.//tr[2]/td/a[1]/text()'))      # 出处
        author = ''.join(li.xpath('.//tr[2]/td/a[2]/text()'))       # 作者
        desc = ''.join(li.xpath('.//tr[3]/td//text()'))             # 简介
        item['articleList'].append(
            {
            'title':title,
            'url':content_url,
            'sources':sources,
            'author':author,
            'desc':desc
            }
        )
    return item


'''中国知网'''
def get_zhiwang(keyword,searchtype='Content'):
    # Content:全文搜索   Theme:主题搜索     Author:作者搜索   KeyWd:关键词搜索

    url = 'https://search.cnki.com.cn/Search/Result'
    data = {
        'searchtype': 'MulityTermsSearch',
        searchtype: keyword,
        'Order': '1',
            }

    html_text = requests.post(url, headers=get_ua(), data=data).text
    e = etree.HTML(html_text)
    recordcount = e.xpath('//*[@id="hidTotalCount"]/@value')[0]


    item = {}
    item['articleList'] = []
    item['success'] = True
    item['recordcount'] = int(recordcount)
    if e.xpath('//*[@class="no-result"]') and int(recordcount)==0:
        item['success'] = False
        return item

    for li in e.xpath('//div[@class="lplist"]/div[@class="list-item"]'):
        title = li.xpath('./p[1]/a[1]/@title')[0]
        content_url = 'https:'+''.join(li.xpath('./p[1]/a[1]/@href'))
        desc = ''.join(li.xpath('./p[@class="nr"]/text()'))
        author = ''.join(li.xpath('./p[@class="source"]/span[1]/@title'))
        sources = ''.join(li.xpath('./p[@class="source"]//text()')).replace('\r\n','').replace('   ','').strip()

        item['articleList'].append(
            {
            'title':title,
            'sources':sources,
            'url':content_url,
            'author':author,
            'desc':desc
            })


    return item


'''万方数据网（代码已过期）'''
def get_wanfang(keyword,searchtype='Content'):

    url = 'http://www.wanfangdata.com.cn/search/searchList.do?'
    searchItem = {
        'Content':'',
        'Theme':'题名:',
        'Author':'作者:',
        'KeyWd':'关键词:'
    }
    params = {
        'searchtype': 'all',
        'showType': 'detail',
        'pageSize': '20',
        'searchWord': searchItem.get(searchtype)+keyword,
        'isTriggerTag':None,
    }
    html = requests.get(url,params=params,headers=get_ua()).text
    e = etree.HTML(html)
    item = {}
    item['success'] = True
    if not e.xpath('//div[@class="BatchOper_result_show"]'):
        print('no kw !')
        item['success'] = False
        item['recordcount'] = 0
        return
    recordcount = e.xpath('//div[@class="BatchOper_result_show"]/span/text()')[0]
    item['recordcount'] = int(recordcount)
    item['articleList'] = []

    for li in e.xpath('//div[@class="ResultCont"]'):
        title = ''.join(li.xpath('./div[@class="title"]/a[1]//text()'))
        content_url ='http://www.wanfangdata.com.cn'+''.join(li.xpath('./div[@class="title"]/a[1]/@href'))
        desc = ''.join(li.xpath('./div[@class="summary"]//text()'))
        author = ' '.join(li.xpath('./div[@class="ResultMoreinfo"]/div[@class="author"]//a/text()'))
        source = ''.join((li.xpath('./div[@class="ResultMoreinfo"]/div[@class="Source"]//a/text()')))
        data = ''.join((li.xpath('./div[@class="ResultMoreinfo"]/div[@class="Volume"]//a/text()')))
        sources = source+' '+data
        item['articleList'].append(
            {
            'title':title,
            'url':content_url,
            'sources':sources,
            'author':author,
            'desc':desc
            })

    return item


# Content:全文搜索   Theme:主题搜索     Author:作者搜索   KeyWd:关键词搜索
'''Jstor'''
def get_jstor(keyword,searchtype='Content'):
    searchItem = {
        'Content':'Query',
        'Theme':'title',
        'Author':'au',
        'KeyWd':'Query'
    }
    url = 'https://www.jstor.org/search-results/grouped-search/'
    if searchtype != 'Content':
        keyword = str("{}:{}".format(searchItem.get(searchtype),keyword))
    data = {"acc": "", "endDate": "", "filter": "",
            "forwardedAdvancedSearchParams": {"Query": keyword},
            "isAdvancedSearch": False,
            "msFacetFields": [{"field": "cty", "efq": []}, {"field": "disc", "efq": []}],
            "pageParams": {},
            "refreqid": "",
            "searchTerm": keyword,
            "sortOrder": "rel",
            "startDate": ""
            }
    json_text = requests.post(url,json= data,headers=get_ua()).json()
    item = {}
    item['success'] = True
    item['recordcount'] = int(json_text['totalResultCount'])

    if item['recordcount']==0:
        item['success'] = False
        return item

    textResults = json_text['textResults']['results']
    item['articleList'] = []
    for li in textResults:
        author = li['author']
        title = li['title']
        stable_url = li['stable_url']
        content_url = 'https://www.jstor.org' + stable_url
        try:
            publisher = li.get('publisher')[0].get('publisher')
        except:
            publisher = ''

        sources = li['tb']+li.get('tbsub') + publisher + str(li.get('publication_year'))
        desc = None

        item['articleList'].append(
            {
            'title':title,
            'url':content_url,
            'sources':sources,
            'author':author,
            'desc':desc
            })

    return item


'''Zlibraty'''
def get_zlibraty(keyword,searchtype='Content'):
    url = 'https://booksc.xyz/s/{}'.format(keyword)
    html = requests.get(url=url, headers=get_ua()).text
    e = etree.HTML(html)
    item = {}
    item['success'] = True
    item['recordcount'] = int(e.xpath('//span[@class="totalCounter"]/text()')[0][1:-1].replace('+',''))
    if item['recordcount'] == 0:
        item['success'] = False
        return item
    item['articleList'] = []
    for li in e.xpath('//div[@id="searchResultBox"]/div[@class="resItemBox resItemBoxArticles exactMatch"]'):
        title = li.xpath('./div//h3/a/text()')[0]
        content_url = 'https://booksc.xyz'+li.xpath('./div//h3/a/@href')[0]

        author = ''.join(li.xpath('./div//div[@class="authors"]/a/text()'))
        sources = ''.join(li.xpath('./div//div[@class="bookDetailsBox"]/div[1]/div[2]//text()'))
        item['articleList'].append(
            {
            'title':title,
            'url':content_url,
            'sources':sources,
            'author':author,
            'desc':None
            })
    return item




'''oalib'''
def get_oalib(keyword,searchtype='Content'):
    searchItem = {
        'Content':'All',
        'Theme':'title',
        'Author':'authors',
        'KeyWd':'keyword'
    }
    searchField = searchItem.get(searchtype)
    url = 'http://www.oalib.com/search?kw={}&searchField={}&pageNo=1'.format(keyword,searchField)
    html = requests.get(url=url,headers=get_ua()).text
    item = {}
    item['success'] = True
    item['totalcount'] = int(re.findall(r'找到相关结果约(.*?)条',html,re.S)[0])
    if item['totalcount'] == 0:
        item['success'] = False
        return item
    e = etree.HTML(html)
    item['articleList'] = []
    for li in e.xpath('//*[@id="form1"]/div//tr[2]/td//tr/td[2]/div[3]//tr/td'):
        href = li.xpath('./span[1]/a/@href')
        if not href:
            continue
        content_url = 'http:'+href[0]

        title = ''.join(li.xpath('./span[1]/a/u//text()'))
        author = ''.join(li.xpath('./span[2]//text()'))
        sources = ''.join(li.xpath('./a/u/text()'))
        date = ''.join(re.findall('\S',''.join(li.xpath('./text()')),re.S))
        desc = ''.join(li.xpath('./div/span[@class="menuContent"]/text()'))[1:].strip()
        item['articleList'].append(
            {
            'title':title,
            'url':content_url,
            'sources':sources+date,
            'author':author,
            'desc':desc
            })
    return item

