#解析每一个章节中的内容

from lxml import etree
import requests
import save
import json
import time

HEADER = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'Accept-Encoding':' gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
}

store_save = []
times = 0

def classify(book_name,webName,store,store_old):
    global store_save
    global times
    store_save = store_old
    for i in range(len(store)):
        title = store[i]['title']
        urlList = store[i]['urlList']
        times = 0
        # 因为该网站有点特殊，章节之间有分几页所以添加一个函数
        if webName == 'ikuaiyan':
            global chapter
            chapter = []
            aba_ikuaiyan(webName,book_name,title,urlList)
        else:
            analysis(webName,book_name,title,urlList)
        if i % 7 == 0: time.sleep(2)
    save.save(book_name,store_save)

#解析规则

with open('static/rules.json', 'r', encoding='utf-8')as fp:
    rules = json.load(fp)

#解析每个章节的内容
def analysis(webName,book_name,title,urlList):
    global times
    html = etree.HTML(requests.get(urlList,HEADER).content.decode(rules[webName]['code'],errors='ignore'))
    chapter = html.xpath(rules[webName]['chapter'])
    if chapter == []:
        times+=1
        if times>=50:
            chapter=['无']
        else:
            analysis(webName,book_name,title,urlList)
            return
    chapter_cont = ''
    for i in chapter:
        if len(i) >= 2:
            chapter_cont = chapter_cont + "\n" + i.strip()
    storeList = {
        "title":title,
        "store":chapter_cont
    }
    store_save.append(storeList)
    save.save(book_name,store_save)
    print(title+"----保存成功")
    return store_save

def aba_ikuaiyan(webName,book_name,title,urlList):
    global times
    global chapter
    html = etree.HTML(requests.get(urlList,HEADER).content.decode(rules[webName]['code'],errors='ignore'))
    all_page = html.xpath('//div[@class="reader-main"]//h1//text()')[0].replace('）', '').split('（')[1].split('/')
    now_page = int(all_page[0])
    max_page = int(all_page[1])
    while(now_page <= max_page):
        text = html.xpath(rules[webName]['chapter'])
        for cont in text:
            chapter.append(cont)
        if now_page == max_page:break
        url = 'http://www.ikuaiyan.com'+html.xpath('//div[@class="read_nav"]//a[@id="next_url"]/@href')[0]
        aba_ikuaiyan(webName, book_name, title, url)
        return
    if chapter == []:
        times+=1
        if times>=50:
            chapter=['无']
        else:
            analysis(webName,book_name,title,urlList)
            return
    chapter_cont = ''
    for i in chapter:
        if len(i) >= 2:
            chapter_cont = chapter_cont + "\n" + i.strip()
    storeList = {
        "title":title,
        "store":chapter_cont
    }
    store_save.append(storeList)
    save.save(book_name,store_save)
    print(title+"----保存成功")
    return store_save
