# -*- coding: utf-8 -*-
# @Author  : lx

# 模拟1688(跨境产品开发工具)滑块验证码案例
import time
import requests
import ssl
import json
from pynput.mouse import Button, Controller as c1

ssl._create_default_https_context = ssl._create_unverified_context

post_url = 'https://overseas.1688.com/api/pdt/search-offers?'
imgUrl = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1594984956317&di=e1a09dc8340c4d2c37c4b76b2d0a3bb7&imgtype=0&src=http%3A%2F%2Fa2.att.hudong.com%2F36%2F48%2F19300001357258133412489354717.jpg'
params = 'imgUrl={}&region=&keyword=&categoryId=-1&location=&tags=&pageNo=1'.format(imgUrl)

cookie2 = "cookie2=331a25fca35bc67921031bce9135f187"	# 可能已过期

url = post_url+params
headers = {
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "referer":"https://kj.1688.com/pdt_tongkuan.html?spm=a262gg.9720235.j6h9wmfu.4485.33241c9bNmbQIu",
    "origin":"origin: https://kj.1688.com",
    "accept-encoding": "gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cookie":"cookie2=331a25fca35bc67921031bce9135f187; hng=CN%7Czh-CN%7CCNY%7C156; t=9b7281f547689832726e554c045762ef; _tb_token_=e3ea0e6a678d1; cna=dKlvFw1+21oCAXt6hjJE/rcC; ali_apache_tracktmp=c_w_signed=Y; __rn_alert__=false; __cn_logon__=true; _csrf_token=1594996218768; cookie1=BqJiuZGjLhWLJPY%2BZhRf3CQs%2ByNkNf6YSsNrYTExEr4%3D; cookie17=UNN0kUGwT5Y%3D; sg=%E6%B0%B406; csg=7bd52f57; lid=%E4%B8%89%E6%9C%A8%E9%87%91%E6%B0%B4; unb=33983330; uc4=nk4=0%40qRFRn4g9SIQTzvh6JET7Rvlm2w%3D%3D&id4=0%40UgQ8eu3x6U1vXyN4UQqkH49WbQ%3D%3D; __cn_logon_id__=%E4%B8%89%E6%9C%A8%E9%87%91%E6%B0%B4; ali_apache_track=c_mid=b2b-33983330|c_lid=%E4%B8%89%E6%9C%A8%E9%87%91%E6%B0%B4|c_ms=1; _nk_=%5Cu4E09%5Cu6728%5Cu91D1%5Cu6C34; last_mid=b2b-33983330; _is_show_loginId_change_block_=b2b-33983330_false; _show_force_unbind_div_=b2b-33983330_false; _show_sys_unbind_div_=b2b-33983330_false; _show_user_unbind_div_=b2b-33983330_false; UM_distinctid=1735d337ac616-0302edb029bc2c-3e3e5c0e-144000-1735d337ac7cc; taklid=e502f6bd97fb4ea2bb0fe00e699b34e4; alicnweb=touch_tb_at%3D1595001167448%7Clastlogonid%3D%25E4%25B8%2589%25E6%259C%25A8%25E9%2587%2591%25E6%25B0%25B4; l=eBgcEiNIOLUg0LBjBO5ahurza779yKRjfsPzaNbMiInca6CfwIwBJNQqhprvkdtjgt5fvHxzPGOpjReWWc4LRA9AWMzSRhXvXLp6-e1..; isg=BCAglmUVa3KZENd27HItm3Bl8S7yKQTzrtHzP5o5WDqIlde_UDt-gzvrLT0VJbzL"
}


def doGetGzip(url,headers):
    content = requests.get(url,headers=headers).text
    return content


s=0
while 1:
    result = json.loads(doGetGzip(url, headers))
    try:
        print(result.get('data').get('trace'))
        s+=1
        print(s)
        import time
    except:
        print(result)
        if result.get('error')=='require login':
            continue
        from selenium import webdriver
        option = webdriver.ChromeOptions()
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        option.add_argument('--user-agent={}'.format(ua))

        driver = webdriver.Chrome(chrome_options=option)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
                        """ })
        driver.set_page_load_timeout(3)
        try:
            driver.get(result['url'])
        except:
            driver.execute_script('window.stop()')
        mouse = c1()
        time.sleep(2)
        # print(mouse.position)         # 可以手动把鼠标放到滑块，测试一下位置
        mouse.position = (564, 449)     # 滑块位置,需要根据自己电脑来修改
        time.sleep(2)
        mouse.press(Button.left)        # 点击左键
        time.sleep(1)
        mouse.move(831, 448)            # 移动到
        mouse.release(Button.left)
        time.sleep(2)
        driver.refresh()       			# 验证成功后刷新获取ck
        cookie_list = driver.get_cookies()
        cookies = ""
        driver.close()
        driver.quit()
        for ck in cookie_list:
            cookies += '{}={}; '.format(ck['name'],ck['value'])
        headers['cookie'] = cookie2+cookies
        print("New Cookies >>>:",cookies)	# 打印出新的cookie
        break
