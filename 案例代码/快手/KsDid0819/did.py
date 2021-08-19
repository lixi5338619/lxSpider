# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 13:11
# @Author  : lx
# @IDE ：PyCharm

import time
import requests
from io import BytesIO
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver import ActionChains

def get_distance(fg, bg):
    """
    计算滑动距离
    """
    target = cv2.imdecode(np.asarray(bytearray(fg.read()), dtype=np.uint8), 0)
    template = cv2.imdecode(np.asarray(bytearray(bg.read()), dtype=np.uint8), 0)
    result = cv2.matchTemplate(target, template, cv2.TM_CCORR_NORMED)
    _, distance = np.unravel_index(result.argmax(), result.shape)
    return distance


def get_did():
    # TODO 修改driver_path
    print("开始获取did...")
    check_url = 'https://www.kuaishou.com/?utm_source=aa&utm_medium=05&utm_campaign=aa_05_pp_yr&plan_id=138090084&unit_id=5205658029&creative_id=43661481717&keyword_id=202928513388&keyword=202928513388&bd_vid=8380158842241119439'
    driver_path=r'C:\Users\feiyi\Desktop\driver\chromedriver.exe'
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')  # 不需要GPU加速
    option.add_argument('--no-sandbox')   # 无沙箱
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument("disable-blink-features")
    option.add_argument("disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=option,executable_path=driver_path)
    driver.get(check_url)
    time.sleep(2)
    try:
        driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[2]/iframe'))
    except:
        driver.delete_cookie('did')
        driver.refresh()
        time.sleep(2)
        driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[2]/iframe'))

    bg_url = driver.find_element_by_class_name('bg-img').get_attribute('src')
    fg_url = driver.find_element_by_class_name('slider-img').get_attribute('src')
    r = requests.get(fg_url, verify=False)
    fg = BytesIO(r.content)
    r = requests.get(bg_url, verify=False)
    bg = BytesIO(r.content)
    distance = get_distance(fg,bg)

    slider = driver.find_element_by_class_name('slider-shadow')
    ActionChains(driver).click_and_hold(slider).perform()
    ActionChains(driver).move_by_offset(distance, 0).perform()
    ActionChains(driver).release().perform()

    did = driver.get_cookies()[0]['value']

    driver.close()
    driver.quit()
    return did
