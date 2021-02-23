# -*- coding: utf-8 -*-
# @IDE ：PyCharm

import requests
from lxml import etree
from lxpy import DateGo

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
}

def cebpubservice():
    url = 'http://www.cebpubservice.com/monitorindustry/monitorplat/index.shtml'
    doc = requests.get(url=url, headers=headers).content.decode('utf-8')
    e = etree.HTML(doc)
    for li in (e.xpath('//div[@class="newslist"]/ul/ul/li')):
        publishTime = ''.join(li.xpath('./span/text()'))
        title = ''.join(li.xpath('./a/span/text()'))
        link = 'http://www.cebpubservice.com'+''.join(li.xpath('./a/@href'))
        news = {}
        news['title'] = title
        news['contentUrl'] = link
        news['publishTime'] = publishTime
        news['realSource'] = '中国招标投标公共服务平台'
        print(news)



def baidu_news():
    for page in range(3):
        url = f'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word=招标&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn={page*10}'
        response = etree.HTML(requests.get(url=url,headers=headers).text)
        result_list = response.xpath('//div[@id="content_left"]//div[@class="result-op c-container xpath-log new-pmd"]')
        for li in result_list:
            news = {}
            news['title'] = ''.join(li.xpath('./div/h3/a//text()'))
            news['contentUrl'] = li.xpath('./div/h3/a/@href')[0]
            news['realSource'] = ''.join(li.xpath('.//span[@class="c-color-gray c-font-normal c-gap-right"]/text()'))
            date = ''.join(li.xpath('.//span[@class="c-color-gray2 c-font-normal"]/text()'))
            if len(date) < 10:
                news['publishTime'] = DateGo.weibo_date(date)
            else:
                news['publishTime'] = (date.replace('年', '-').replace('月', '-').replace('日', ' ') + ':00').replace('  ',' ')
            print(news)