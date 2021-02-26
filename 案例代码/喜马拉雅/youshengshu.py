# -*- coding:utf-8 -*-

import hashlib
import json
import os
import re
import time
import random
import requests

'''有声书下载'''
class ximalaya(object):
    def __init__(self):
        self.base_url = 'https://www.ximalaya.com'
        self.base_api = 'https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&sort=0&pageSize=30'
        self.time_api = 'https://www.ximalaya.com/revision/time'
        self.header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}
        self.s = requests.session()


    def get_time(self):
        """
        获取服务器时间戳
        :return:
        """
        r = self.s.get(self.time_api, headers=self.header)
        return r.text


    def get_sign(self):
        """
        获取sign： md5(服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
        :return: xm_sign
        """
        nowtime = str(round(time.time() * 1000))
        servertime = self.get_time()
        sign = str(hashlib.md5("himalaya-{}".format(servertime).encode()).hexdigest()) + "({})".format(
            str(round(random.random() * 100))) + servertime + "({})".format(str(round(random.random() * 100))) + nowtime
        self.header["xm-sign"] = sign


    def index_choose(self):
        xm_id = input(u'请输入要获取喜马拉雅节目的ID：')
        xima.get_fm(xm_id)
        self.index_choose()

    @staticmethod
    def make_dir(xm_fm_id):
        # 保存路径，请自行修改，这里是以有声书ID作为文件夹的路径
        fm_path = './{}'.format(xm_fm_id)
        f = os.path.exists(fm_path)
        if not f:
            os.makedirs(fm_path)
            print('make file success')
        else:
            print('file already exists')
        return fm_path


    def get_fm(self, xm_fm_id,lable='youshengshu'):
        # 根据有声书ID构造url
        fm_url = self.base_url + '/{}/{}'.format(lable,xm_fm_id)
        r_fm_url = self.s.get(fm_url, headers=self.header)
        fm_title = re.findall('<h1 class="title vA_">(.*?)</h1>', r_fm_url.text, re.S)[0]
        print('书名：' + fm_title)
        # 新建有声书ID的文件夹
        fm_path = self.make_dir(xm_fm_id)
        # 取最大页数
        s = re.findall(r'/{}/{}/p(\d+)/'.format(lable,xm_fm_id), r_fm_url.text, re.S)
        max_page = sorted([int(i) for i in s])[-1]

        if max_page:
            for page in range(1, int(max_page) + 1):
                print('第' + str(page) + '页')
                self.get_sign()
                r = self.s.get(self.base_api.format(xm_fm_id, page), headers=self.header)
                r_json = json.loads(r.text)
                for audio in r_json['data']['tracksAudioPlay']:
                    audio_title = str(audio['trackName']).replace(' ', '')
                    audio_src = audio['src']
                    self.get_detail(audio_title, audio_src, fm_path)
                # 每爬取1页，30个音频，休眠3秒
                time.sleep(3)
        else:
            print(os.error)

    def get_detail(self, title, src, path):
        r_audio_src = self.s.get(src, headers=self.header)
        m4a_path = path+'/' + title + '.m4a'
        if not os.path.exists(m4a_path):
            with open(m4a_path, 'wb') as f:
                f.write(r_audio_src.content)
                print(title + '保存完毕...')
        else:
            print(title + 'm4a已存在')


if __name__ == '__main__':
    xima = ximalaya()
    xima.index_choose()
    # 12576446
