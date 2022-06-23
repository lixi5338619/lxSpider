'''https://www.cnvd.org.cn/flaw/list.htm'''

'''cookie加密，前两次请求返回js文件设置cookie，最后一次请求内容'''
import requests
import re
import execjs
from bs4 import BeautifulSoup
import time
import random
from loguru import logger

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'

}

sess = requests.session()

url = 'https://www.cnvd.org.cn/flaw/list.htm'

def get1():
    r =sess.get(url,headers=headers,timeout=15,verify=False)
    logger.info(f'第一次请求：{r.status_code}')
    text = r.text
    cookie = re.search('<script>document.cookie=(.*?);location',text).group(1)
    x = execjs.eval(cookie).split(';')[0].split('=')
    sess.cookies[x[0]] = x[1]

def get2():
    '''获取第二次请求的cookie'''
    r1 = sess.get(url,headers=headers,verify=False)
    logger.info(f'第二次请求：{r1.status_code}')
    text = r1.text
    print(text)
    data = re.search(';go\((.*?)\)</script>',text).group(1)
    print(data)
    hash = re.search('"ha":"(.*?)",',data).group(1)
    cookie = get_cookie_2(data,hash).split(';')[0].split('=')
    sess.cookies[cookie[0]] =cookie[1]


def get3(i):
    # r =sess.get(url,headers=headers,verify = False)
    # print(r.status_code)
    # text = r.text
    # # 解析页面
    # parse(text)

    data = {'number': '请输入精确编号', 'startDate': '', 'endDate': '', 'field': '', 'order': '', 'numPerPage': '10', 'offset': i*10, 'max': '10'}
    r1 = sess.post('https://www.cnvd.org.cn/flaw/list.htm?flag=true',headers=headers,data=data,verify=False)
    logger.info(f'第三次请求：{r1.status_code}')
    parse(r1.text)
    time.sleep(random.random())

def parse(text):
    soup = BeautifulSoup(text, 'lxml')
    table = soup.find('table', class_='tlist').tbody
    tr_list = table.find_all('tr', recursive=False)
    for tr in tr_list:
        td_list = tr.find_all('td', recursive=False)
        for td in td_list:
            print(td.text.strip(), end='\t')
        print()


def get_cookie_2(data,hash):
    node = execjs.get()
    path=rf'./t_{hash}.js'
    with open(path,'r',encoding='utf-8') as f:
        #2.js源文件编译
        ctx = node.compile(f.read())
        #3.执行js函数
        funcName = f'go({data})'
        pwd = ctx.eval(funcName)
        return pwd

if __name__ == '__main__':
    get1()
    get2()
    for i in range(80,81):
        try:
            # 如果cookie过期
            get3(i)
        except:
            # 重新建立session，并设置cookie
            sess = requests.session()
            get1()
            get2()
            # 重新请求失败的页面
            get3(i)