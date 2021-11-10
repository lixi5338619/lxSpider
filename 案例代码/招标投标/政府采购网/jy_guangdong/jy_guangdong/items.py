# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# tos_code         业务类型编码=====================
# 01    工程建设
# 02    政府采购
# 03    土地使用权
# 05    国有产权
# 90    其他

# notice_type_code 信息类型编码=====================
# 工程建设
# 0101    招标/资审公告
# 0102    开标记录
# 0104    交易结果公示
# 0105    招标/资审文件澄清
# 0106    资格预审结果
# 政府采购
# 0201    采购/资审公告
# 0202    中标公告
# 0203    采购合同
# 0204    更正事项
# 土地使用权
# 0301    出让公示
# 0302    成交宗地
# 国有产权
# 0501    挂牌披露
# 0502    交易结果
# 其他
# 9001    交易公告
# 9002    成交公示

# area_code 地区编码(省级部分，详细：t_sys_area)====================
# "北京": "11",
# "天津": "12",
# "河北": "13",
# "山西": "14",
# "内蒙古": "15",
# "辽宁": "21",
# "吉林": "22",
# "黑龙江": "23",
# "上海": "31",
# "江苏": "32",
# "浙江": "33",
# "安徽": "34",
# "福建": "35",
# "江西": "36",
# "山东": "37",
# "河南": "41",
# "湖北": "42",
# "湖南": "43",
# "广东": "44",
# "广西": "45",
# "海南": "46",
# "重庆": "50",
# "四川": "51",
# "贵州": "52",
# "云南": "53",
# "西藏": "54",
# "陕西": "61",
# "甘肃": "62",
# "青海": "63",
# "宁夏": "64",
# "新疆": "65",
# "台湾": "71",
# "香港特别行政区": "81",
# "澳门特别行政区": "82",


class CommonRawItem(scrapy.Item):
    # _id: 公告唯一标识，算法: md5(公告正文链接)
    # area: 公告地点(省份)，中文，例如：北京、四川
    # area_detail：公告地点（地市），中文，例如：南京、南通
    # notice_time: 格式固定为 2019.02.02 21:21:21
    # buyer:  采购人，中文，例如：中央电视台
    # notice_type: 公告类型，中文，如：更正公告、中标候选人公示
    # tos: 业务类型，中文，如：工程建设，政府采购，土地使用权, 矿业权, 药品采购等
    # site:   网站的domain, 例如：hljggzyjyw.gov.cn
    # source：信息来源细分，比如：http://www.ccgp.gov.cn/ 分为中央公告和地方公告
    # title：公告标题，中文
    # url：公告正文连接，如：http://www.ccgp.gov.cn/cggg/zygg/gzgg/201902/t20190202_11610905.htm
    # content：公告正文，base64(zlib(原文))

    # 唯一标识, 用来数据排重，一般取url全路径的md5
    _id = scrapy.Field()

    # 网站地址, 例如：ccgp.gov.cn
    site = scrapy.Field()

    # 网站中文名, 例如：中国政府采购网
    site_name = scrapy.Field()

    # 公告来源，如：中央公告
    source = scrapy.Field()

    # 标题
    title = scrapy.Field()

    # 原文地址
    url = scrapy.Field()

    # 地区，如：江苏
    area = scrapy.Field()

    # 地区，如：南通
    area_detail = scrapy.Field()

    # 地区编码，符合表:t_sys_area定义，如："北京": "11"、"江苏": "32"
    area_code = scrapy.Field()

    # 公告类型中文，如：成交公告
    notice_type = scrapy.Field()

    # 公告类型编码，如：0101
    notice_type_code = scrapy.Field()

    # 业务类型中文，如：政府采购
    tos = scrapy.Field()

    # 业务类型编码，如：01
    tos_code = scrapy.Field()

    # 公告时间
    notice_time = scrapy.Field()

    # 采购人
    buyer = scrapy.Field()

    # 正文内容
    content = scrapy.Field()

    # 正文内容生成方式：1 - 原文; 2 - 拼接生成
    content_code = scrapy.Field()

    # 时间戳
    time_stamp = scrapy.Field()

    # 行业类型
    industry = scrapy.Field()
