# -*- coding: utf-8 -*-

import requests
import time
h = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
c = {
    'sid':'你的sid，不填等程序更新也行',
    'captui':'你的captui，不填等程序更新也行'
}
q = 'lx'

url = f'https://www.researchgate.net/search/researcher?q={q}'
d = requests.get(url, headers=h,cookies=c)
if d.status_code == 429:
    print("cookies validation failed")
    # 接下来应该进行验证，获取 cattui 后构建cookie，再次请求
    # capUrl = f'https://www.researchgate.net/application.ClientValidation.html?origPath=/search/researcher?q={q}'
    # cookies = requests.utils.dict_from_cookiejar(d.cookies)
    # d = requests.get(capUrl, headers=h,cookies=cookies)
    # 但是因为没外网，获取不到验证，这里采用其他方式获取新cookie，
    # TODO 记得修改 executable_path
    from selenium import webdriver
    driver = webdriver.Chrome(executable_path=r'C:\Users\feiyi\Desktop\chromedriver.exe')
    driver.get(url)
    time.sleep(5)
    cookies = {}
    for cook in driver.get_cookies():
        cookies[cook['name']]=cook['value']
    c.update(cookies)

d = requests.get(url, headers=h,cookies=c)


from lxml import etree
e = etree.HTML(d.text)
for li in e.xpath('//div[@class="nova-v-person-item__body"]'):
    print(li.xpath('./div/div[1]/a/img/@src'))
...