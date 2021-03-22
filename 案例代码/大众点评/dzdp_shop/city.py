# -*- coding:utf-8 -*-
import requests
from lxml import etree
import time
import re
from fontTools.ttLib import TTFont


session = requests.session()
words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下澩凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'


def get_regex_data(regex, buf):
    """
    正则表达式
    :param regex: 正则语法
    :param buf: html源代码
    :return:
    """
    group = re.search(regex, buf)
    if group:
        return group.groups()[0]
    else:
        return ''


def get_xpath(xpath, content):
    """
    xpayh 获取具体字段 或 table
    :param xpath:  xpath语法
    :param content:  页面源代码
    :return: list
    """
    out = []
    tree = etree.HTML(content)
    results = tree.xpath(xpath)
    for result in results:
        if 'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)):
            out.append(result)
        else:
            out.append(etree.tostring(result))
    return out


def get_city(city_name):
    url = 'https://www.dianping.com/citylist'
    response = session.get(url, headers=headers).content.decode()
    city_list = get_xpath('//div[@class="main-citylist"]/ul/li/div[@class="terms"]/div/a', response)
    for cl in city_list:
        name = get_xpath('//a/text()', cl)[0]
        if str(city_name).strip() in name:
            city_url = 'https:'+str(get_xpath('//a/@href', cl)[0]).strip()
            return city_url
        else:
            continue


def leimu(city, leimus):
    city_url = get_city(city)
    time.sleep(2.5)
    city_response = session.get(city_url, headers=headers).content.decode()
    leimu_list = get_xpath('//ul[@class="first-cate J-primary-menu"]/li/div[1]/span/a', city_response)
    for ll in leimu_list:
        ll_name = get_xpath('//a/text()', ll)[0]
        if str(leimus).strip() in ll_name:
            url = str(get_xpath('//a/@href', ll)[0])
            return url
        else:
            continue


def xingzhengqu(city, fenlei):
    url = leimu(city, fenlei)
    time.sleep(2.5)
    print(url)
    response = session.get(url, headers=headers).content.decode()

    # print(response)
    xzq_list = get_xpath('//div[@class="nc-contain"]/div[@id="J_nt_items"]/div[@id="region-nav"]/a', response)
    print(len(xzq_list))

    if len(xzq_list) == 0:
        with open('1.html', 'w', encoding='utf-8') as files:
            files.write(response)
        files.close()
    item = []
    for xl in xzq_list:
        xl_name = get_xpath('//a/span/text()', xl)[0]
        print(xl_name)
        xl_url = get_xpath('//a/@href', xl)[0]
        url_response = session.get(xl_url, headers=headers).content.decode()
        road_list = get_xpath('//div[@class="nc-contain"]/div[@id="J_nt_items"]/div[@id="region-nav-sub"]/a',
                              url_response)
        for rl in road_list:
            rl_name = get_xpath('//a/span/text()', rl)[0]
            if rl_name == '不限':
                continue
            else:
                rl_url = get_xpath('//a/@href', rl)[0]
                table = {}
                table['administrative_region'] = xl_name
                table['administrative_region_url'] = xl_url
                table['street'] = rl_name
                table['street_url'] = rl_url
                item.append(table)
    return item


def get_woff(url):
    print(url)
    response = requests.get(url,headers=headers).content.decode()
    font_list = re.findall('@font-face\{(.*?)\}', response)
    font_dics = {}
    for font in font_list:
        # 正则表达式获取字体文件名称
        font_name = get_regex_data('font-family: "PingFangSC-Regular-(.*?)"', font)
        # 正则表达式获取字体文件对应链接
        font_dics[font_name] = 'http:' + get_regex_data(',url\("(.*?.woff)"\);', font)
    font_use_list = ['shopNum', 'tagName', 'address']
    for key in font_use_list:
        woff = requests.get(font_dics[key], headers=headers).content
        with open(f'{key}.woff', 'wb')as f:
            f.write(woff)


def dict_woff(key):
    real_list = {}
    # 打开本地字体文件
    font_data = TTFont(f'{key}.woff')
    # font_data.saveXML('shopNum.xml')
    # 获取全部编码，前2个非有用字符去掉
    uni_list = font_data.getGlyphOrder()[2:]
    # 请求数据中是 "" 对应 编码中为"uniF8A1",我们进行替换，以请求数据为准
    real_list[key] = ['&#x' + uni[3:] for uni in uni_list]
    return real_list


def merchants(city, fenleis):
    xzq_item = xingzhengqu(city, fenleis)
    time.sleep(2.5)
    for xi in xzq_item:
        administrative_region = xi['administrative_region']
        administrative_region_url = xi['administrative_region_url']
        street = xi['street']
        print('aaa', street)
        street_url = xi['street_url']
        print(street_url)
        response = session.get(street_url,headers=headers).text
        html = get_regex_data('(<div class="content">[\d\D]*?)<div class="page"', response)
        table_list = re.findall('(<li class[\d\D]*?</li>)', html)
        css_url = get_regex_data('(//s3plus\.meituan\.net/.*?)"', response)
        get_woff('http:'+str(css_url).strip())
        real_list = dict_woff('shopNum')
        real_list1 = dict_woff('tagName')
        real_list2 = dict_woff('address')

        items = []
        for x in range(len(real_list['shopNum'])):
            dict_ = {}
            dict_['msg'] = words[x]
            dict_['name'] = real_list['shopNum'][x]
            items.append(dict_)

        items1 = []
        for x in range(len(real_list1['tagName'])):
            dict_ = {}
            dict_['msg'] = words[x]
            dict_['name'] = real_list1['tagName'][x]
            items1.append(dict_)

        items2 = []
        for x in range(len(real_list2['address'])):
            dict_ = {}
            dict_['msg'] = words[x]
            dict_['name'] = real_list2['address'][x]
            items2.append(dict_)

        count = 1
        for tl in table_list:
            if count <= 2:
                count += 1
                continue
            # 店名
            title = get_regex_data('<h4>(.*?)</h4>', tl)
            print(title)
            #  打分
            star_score = get_regex_data('<div class="star_score score_45  star_score_sml">(.*?)</div>', tl)
            print(star_score)
            comment_msg = get_regex_data('<b>(.*?)</b>\s+条评价', tl)
            comments = ''  # 评论数
            comments_list = re.findall('(&#.*?);', comment_msg)
            for cl in comments_list:
                for ix in items:
                    if ix['name'] == cl:
                        comments += str(ix['msg'])
                        break
            print('评论', comments)


            per_capita_msg = get_regex_data('人均\s+<b>(.*?)</b>', tl)
            per_capita = get_regex_data('(.*?)<svgmtsi', per_capita_msg)  # 人均
            per_list = re.findall('>(.*?)<', per_capita_msg)
            for pl in per_list:
                if ';' in pl:
                    for ix in items:
                        if ix['name'] == pl[0:-1]:
                            per_capita += str(ix['msg'])
                            break
                else:
                    per_capita += str(pl)
            print('人均',  per_capita)

            cuisine_msg = get_regex_data('data-click-name="shop_tag_cate_click".*?>(.*?</span>)', tl)
            cuisine = get_regex_data('<span class="tag">(.*?)<svgmtsi', cuisine_msg)  # 菜系
            cuisine_list = re.findall('>(.*?)<', cuisine_msg)
            for cm in cuisine_list:
                if ';' in cm:
                    for ix in items1:
                        if ix['name'] == cm[0:-1]:
                            cuisine += str(ix['msg'])
                            break
                else:
                    cuisine += str(cm)
            print('菜系', cuisine)

            region_msg = get_regex_data('data-click-name="shop_tag_region_click".*?>(.*?</span>)', tl)
            #地区
            region = get_regex_data('<span class="tag">(.*?)<svgmtsi', region_msg)
            region_list = re.findall('>(.*?)<', region_msg)
            for rel in region_list:
                if ';' in rel:
                    for ix in items1:
                        if ix['name'] == rel[0:-1]:
                            region += str(ix['msg'])
                            break
                else:
                    region += str(rel)
            print('地区', region)

            addr_msg = get_regex_data('(<span class="addr">.*?</span>)', tl)
            addr = get_regex_data('<span class="addr">(.*?)<svgmtsi', addr_msg)
            addr_list = re.findall('>(.*?)<', addr_msg)
            for al in addr_list:
                if ';' in al:
                    for ix in items2:
                        if ix['name'] == al[0:-1]:
                            addr += str(ix['msg'])
                            break
                else:
                    addr += str(al)
            print('地址', addr)

            taste_msg = get_regex_data('口味(<b>.*?</b>)', tl)
            # 口味
            taste = ''
            taste_list = re.findall('>(.*?)<', taste_msg)
            for tal in taste_list:
                if ';' in tal:
                    for ix in items:
                        if ix['name'] == tal[0:-1]:
                            taste += str(ix['msg'])
                            break
                else:
                    taste += str(tal)
            print('口味', taste)

            environment_msg = get_regex_data('环境(<b>.*?</b>)', tl)
            # 环境
            environment = ''
            environment_list = re.findall('>(.*?)<', environment_msg)
            for el in environment_list:
                if ';' in el:
                    for ix in items:
                        if ix['name'] == el[0:-1]:
                            environment += str(ix['msg'])
                            break
                else:
                    environment += str(el)
            print('环境', taste)

            service_msg = get_regex_data('服务(<b>.*?</b>)', tl)
            # 服务
            service = ''
            service_list = re.findall('>(.*?)<', service_msg)
            for sl in service_list:
                if ';' in sl:
                    for ix in items:
                        if ix['name'] == sl[0:-1]:
                            service += str(ix['msg'])
                            break
                else:
                    service += str(sl)
            print('服务', service)

            break

        break

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.141 Safari/537.36'
    }

    city_url = merchants('杭州', '美食')
    print(city_url)
