import requests
import json
import numpy as np
import math


# 谷歌地图
# 思路：从一点出发，选取该点最优Z（以整数调整），以该点的切片边长或1d表达式做距离，经纬等长移动度差，移动后的每一点重复该步骤。

# 经纬度和距离互转:来源：https://blog.csdn.net/qq_37742059/article/details/101554565

earth_radius = 6370.856  # 地球平均半径 / 单位km
math_2pi = math.pi * 2
pis_per_degree = math_2pi / 360  # 角度一度所对应的弧度数，360对应2*pi

# 纯纬度上，距离值转度数
def lat_km2degree(dis_km=111, radius=earth_radius):
    """
    通过圆环求法，纯纬度上，距离值转度数(diff)，与中间点所处的地球上的位置关系不大
    :param dis_km: 输入的距离，单位km，经验值111km相差约(接近)1度
    :param radius: 圆环求法的等效半径，纬度距离的等效圆环是经线环，所以默认都是earth_radius
    :return: 这个距离dis_km对应在纯纬度上差多少度
    """
    return dis_km / radius / pis_per_degree


def lng_km2degree(dis_km=1, center_lat=22):
    """
    纯经度上，距离值转角度差(diff)，单位度数。
    :param dis_km: 输入的距离，单位km
    :param center_lat: 中心点的纬度，默认22为深圳附近的纬度值；为0时表示赤道。赤道、中国深圳、中国北京、对应的修正系数分别约为： 1  0.927  0.766
    :return: 这个距离dis_km对应在纯经度上差多少度
    """
    # 修正后，中心点所在纬度的地表圆环半径
    real_radius = earth_radius * math.cos(center_lat * pis_per_degree)
    return lat_km2degree(dis_km, real_radius)


def get_allcom(response):
    page_source = response.text
    big_dict = json.loads(page_source.replace('/*""*/', ''))
    d_str = big_dict['d'].replace(")]}'", '').strip()
    d_list = json.loads(d_str)
    return d_list


# 调整1d，moudle1：步幅0.01，moudle0：步幅1
def get_1d(module = 1, offset = 0.01):
    a = []
    # z=2 1d值
    ori = 94618532.08008283
    a.append([2,ori])
    for i in range(2,22):
        if i > 2:
            ori = (ori / 2)
        else:
            ori = ori
        if module == 1:
            for j in np.arange(0,1,offset):
                if (i+j) > 2 and (i+j) <= 21:
                    # print((i+j),ori - ori*j/2)
                    a.append([(i+j),ori - ori*j/2])
        elif module == 0:
            if [i,ori] not in a:
                a.append([i,ori])
    return dict(a)


# 调整经纬度
def get_23d(d2, d3, dis = 5775.056889653493):
    # 默认经纬度步幅，取缩放倍数16的1d
    lat = lat_km2degree(int(dis/1000))
    lon = lng_km2degree(int(dis/1000),d3)
    up = (d2, d3+lat) if d3+lat > -85.05112877980659 and d3+lat < 85.05112877980659 else None
    down = (d2, d3-lat) if d3-lat > -85.05112877980659 and d3-lat < 85.05112877980659 else None
    left = (d2-lon, d3) if d2-lon > -180 and d2-lon < 180 else None
    right = (d2+lon, d3) if d2+lon > -180 and d2+lon < 180 else None
    return[up, down, left, right]


def get_com(d2, d3):
    com_num = {}
    d1_dict = get_1d(0)
    for d1_multiple in d1_dict:
        d1 = d1_dict[d1_multiple]
        print('目前倍数%d：'%d1_multiple)
        url = 'https://www.google.com/search?tbm=map&authuser=0&hl=zh-CN&gl=us&pb=!4m12!1m3!1d{}!2d{}!3d{}'
        page = 0
        all_result = []
        while True:
            q = '餐厅'
            pb = '!2m3!1f0!2f0!3f0!3m2!1i784!2i644!4f13.1!7i20{}!10b1!12m8!1m1!18b1!2m3!5m1!6e2!20e3!10b1!16b1!19m4!2m3!1i360!2i120!4i8!20m57!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m42!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!22m5!1s5mKzXrHAJNSXr7wP5u-akAQ!4m1!2i5600!7e81!12e30!24m46!1m12!13m6!2b1!3b1!4b1!6i1!8b1!9b1!18m4!3b1!4b1!5b1!6b1!2b1!5m5!2b1!3b1!5b1!6b1!7b1!10m1!8e3!14m1!3b1!17b1!20m2!1e3!1e6!24b1!25b1!26b1!30m1!2b1!36b1!43b1!52b1!55b1!56m2!1b1!3b1!65m5!3m4!1m3!1m2!1i224!2i298!26m4!2m3!1i80!2i92!4i8!30m28!1m6!1m2!1i0!2i0!2m2!1i458!2i644!1m6!1m2!1i734!2i0!2m2!1i784!2i644!1m6!1m2!1i0!2i0!2m2!1i784!2i20!1m6!1m2!1i0!2i624!2m2!1i784!2i644!31b1!34m13!2b1!3b1!4b1!6b1!8m3!1b1!3b1!4b1!9b1!12b1!14b1!20b1!23b1!37m1!1e81!42b1!46m1!1e2!47m0!49m1!3b1!50m13!1m8!3m6!1u17!2m4!1m2!17m1!1e2!2z6Led56a7!4BIAE!2e2!3m2!1b1!3b0!59BQ2dBd0Fn!65m0&q={}&tch=1&ech=4&psi=5mKzXrHAJNSXr7wP5u-akAQ.1588814569168.1'
            page_id = '!8i%d'%page
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
            response = requests.get(url.format(d1,d2,d3)+pb.format(page_id,q), headers = headers,proxies=proxies)
            result = get_allcom(response)
            for li in result[0][1][1:]:
                res = li[-1]
                print(res[11], res[18])
            all_result += result
            if len(result) != 0:
                page+=20
            else:
                break
        #print(d1, len(all_result))
        com_num[d1_multiple] = len(all_result)

    max_num = max(list(com_num.values())[12:19])
    if max_num == 0:
        # 新的四个坐标
        new_list = get_23d(d2, d3)
        print('没有最优倍数，取默认值')
    else:
        best_d1_multiple = [i for i in list(com_num.keys())[12:19] if com_num[i] == max_num]
        print('最优倍数为：', best_d1_multiple)
        new_list = get_23d(d2, d3, dis = d1_dict[best_d1_multiple[0]])
    print('移动后的四个坐标',new_list)
    for i in new_list:
        if i:
            get_com(i[0],i[1])


if __name__ == '__main__':
    # 起始点
    proxies = {}
    d2 = 114.1277
    d3 = 22.3527234
    get_com(d2, d3)

    # d3 = 34.817169  # 纬度
    # d2 = 113.535912 # 经度
