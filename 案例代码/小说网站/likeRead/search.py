from lxml import etree
import requests
import win32clipboard as wc
import win32con

def search(name):
    search_web = ["http://www.zxcs.info/index.php?keyword=%s"%name]
    html = etree.HTML(requests.get(search_web[0]).content.decode('utf-8',errors='ignore'))
    title = html.xpath('//dl[@id="plist"]/dt/a//text()')
    url = html.xpath('//dl[@id="plist"]/dt/a/@href')
    if title == []:
        return False
    for i in range(len(title)):
        title[i] = title[i].replace('《','').split('》')[0]
        print(str(i)+":"+title[i])
    print("-"*50)
    index = input('请输入要下载的小说前方的序号：')

    html_deta = etree.HTML(requests.get(url[int(index)]).content.decode('utf-8',errors='ignore'))
    deta_src = 'http://www.zxcs.info'+html_deta.xpath('//p[@class="filetit"]/a/@href')[0]

    html_donw = etree.HTML(requests.get(deta_src).content.decode('utf-8',errors='ignore'))
    donw_src = html_donw.xpath('//span[@class="downfile"]/a/@href')
    for src in donw_src:
        if(src.split('.')[1]=='zxcsdown'):
            print(src)
            wc.OpenClipboard()
            wc.EmptyClipboard()
            wc.SetClipboardData(win32con.CF_UNICODETEXT, src)
            wc.CloseClipboard()
    return True
