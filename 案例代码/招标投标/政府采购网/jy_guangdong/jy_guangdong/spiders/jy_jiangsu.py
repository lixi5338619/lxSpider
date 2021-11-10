# -*- coding: utf-8 -*-
import scrapy
import logging
import logging.handlers
import requests
import zlib
import base64
import time
import random
from scrapy_splash import SplashRequest
from urllib.parse import urlencode, quote_plus
from enum import Enum
from datetime import datetime
import pymongo
import hashlib
import json

import sys

# 以下是杰云相关的包
from jy_scrapy_common.jy_common_items import CommonRawItem
from jy_scrapy_common.jy_utils import JyScrapyUtil
from jy_scrapy_common.jy_crawl_helper import JyCrawlHelper


class CrawlMode(Enum):
    REAL_TIME = 0
    HISTORY = 1


class Jy_jiangsuSpider(scrapy.Spider):
    name = 'jy_jiangsu_spider'  # 需要修改成全局唯一的名字
    allowed_domains = ['www.jszbtb.com']  # 需要修改成爬取网站的域名

    def __init__(self, *args, **kwargs):
        super(Jy_jiangsuSpider, self).__init__(*args, **kwargs)

        self.num = 0
        self.site = self.allowed_domains[0]
        self.crawl_mode = CrawlMode.HISTORY

        # 用来判断数据是否已经入库的mongo表对象
        self.mongo_client = None
        self.mongo_col_obj = None

        self.crawl_helper = None

        # 日志相关
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s')

        # Define a RotatingFileHandler
        rf_handler = logging.handlers.RotatingFileHandler(
            filename='./{}.log'.format(self.name),
            mode='a',
            maxBytes=10 * 1024 * 1024,
            backupCount=20,
        )
        formatter = logging.Formatter('%(asctime)s  %(filename)s:%(lineno)s : %(levelname)s  %(message)s')
        rf_handler.setFormatter(formatter)
        rf_handler.setLevel(logging.INFO)

        # Create an root instance
        logging.getLogger().addHandler(rf_handler)

    def init_crawl_helper(self):
        try:
            if 'spider_name' in self.__dict__:
                spider_name = self.spider_name
            else:
                spider_name = self.name

            _settings = self.settings
            self.mongo_client = pymongo.MongoClient(_settings.get('MONGDB_URI'))
            self.crawl_helper = JyCrawlHelper(
                spider_name=spider_name,
                mongo_client=self.mongo_client,
                db_name=_settings.get('MONGDB_DB_NAME'),
                col_name=_settings.get('MONGDB_COLLECTION'))
        except Exception as e:
            logging.exception('Get get_crawl_helper failed')
            self.crawl_helper = None

    def start_requests(self):
        """
        爬虫默认接口,启动方法
        :return:
        """
        # 获取爬取时传过来的参数
        # start_time: 开始时间
        # end_time: 结束时间
        # start_page: 开始页 (优先于start_time)
        # end_page: 结束页 (优先于end_time)
        # stop_item: 连续遇到[stop_item]个重复条目后，退出本次爬取
        # spider_name: 指定的spider_name，如果不指定，使用self.name
        # command example:
        #       python3 -m scrapy crawl jy_jiangsu_spider -a start_time="2019:01:01" -a end_time="2020:02:26"
        # nohup python3 -m scrapy crawl jy_jiangsu_spider -a start_time="2019:01:01" -a end_time="2020:02:25" > /dev/null&
        # py -3 -m scrapy crawl base_spider -a start_time="now" -a end_time="now"
        # py -3 -m scrapy crawl base_spider -a start_time="now" -a end_time="now" -a start_page="700" -a end_page="1000" -a stop_item="10000"
        assert self.start_time is not None
        assert self.end_time is not None

        self.crawl_mode = CrawlMode.REAL_TIME if str(self.start_time).lower() == 'now' else CrawlMode.HISTORY

        if self.crawl_mode == CrawlMode.HISTORY:
            if (len(self.start_time) != 10 or len(self.end_time) != 10
                    or self.start_time[4] != ':' or self.end_time[4] != ':'):
                logging.error('Bad date format start_time:[{}] end_time:[{}]. Example: 2019:01:01'.format(
                    self.start_time, self.end_time))
                return
        else:
            # 取当天日期
            _dt = datetime.fromtimestamp(time.time())
            self.start_time = _dt.strftime("%Y:%m:%d")
            self.end_time = self.start_time

        # 初始化self.crawl_helper
        self.init_crawl_helper()

        # 主要配置项
        _source_info = {
            # 页面的key，保证唯一
            'page_1': {
                # 通常会被填充在'source'字段里，有时也可以放在'tos'
                'name': '江苏省招标投标公共服务平台',

                # list页面的base地址
                'base_url': 'http://api.jszbtb.com/DataSyncApi/HomeQulifyBulletin?',

                # list页面的call_back处理函数
                'callback': self.parse_list_page_common,

                'method': "get",

                'requests_type': "dict",

                # 得到下一页url的函数，返回值一定是一个url
                'get_next_page_url': self.get_normal_next_page_url,

                # 网站中该页面的最大页数，（可选配置，仅为优化程序执行效率，可不填）
                'stop_page_num': 1000,

                # 连续遇到[stop_dup_item_num]个重复条目后，停止本次抓取
                # 提示：在程序运行初始阶段，此值可以设的较大，以便爬取所有的历史记录
                'stop_dup_item_num': 500000 if self.crawl_mode == CrawlMode.HISTORY else 60,

                # list页面中，获得条目列表的xpath
                'xpath_of_list': ['data', 'data'],

                # 获得每一个条目链接地址的xpath
                'xpath_of_detail_url': 'id',

                # 对每一个条目进行解析，返回CommonRawItem的类，需要实现
                'item_parse_class': BaseItemCommonParser,

                # 其它信息，可以辅助生成CommonRawItem的字段
                # 参考函数parse_list_page_common() 中 item_parser.get_common_raw_item()代码
                'tos': '工程建设',
                'tos_code': '01',
                'source': '江苏省招标投标公共服务平台',
                'notice_type': "采购公告",
                'notice_type_code': '0101',
                'area_code': '32',
                'content_code': '1',
                'site_name': '江苏省招标投标公共服务平台',
                'industry': '工程建设',
                'bid_type': 'QulifyBulletin',
                'time_type': 6 if self.crawl_mode == CrawlMode.HISTORY else 0,
            },
            'page_2': {
                # 通常会被填充在'source'字段里，有时也可以放在'tos'
                'name': '江苏省招标投标公共服务平台',

                # list页面的base地址
                'base_url': 'http://api.jszbtb.com/DataSyncApi/HomeTenderBulletin?',

                # list页面的call_back处理函数
                'callback': self.parse_list_page_common,

                'method': "get",

                'requests_type': "dict",

                # 得到下一页url的函数，返回值一定是一个url
                'get_next_page_url': self.get_normal_next_page_url,

                # 网站中该页面的最大页数，（可选配置，仅为优化程序执行效率，可不填）
                'stop_page_num': 1000,

                # 连续遇到[stop_dup_item_num]个重复条目后，停止本次抓取
                # 提示：在程序运行初始阶段，此值可以设的较大，以便爬取所有的历史记录
                'stop_dup_item_num': 500000 if self.crawl_mode == CrawlMode.HISTORY else 60,

                # list页面中，获得条目列表的xpath
                'xpath_of_list': ['data', 'data'],

                # 获得每一个条目链接地址的xpath
                'xpath_of_detail_url': 'id',

                # 对每一个条目进行解析，返回CommonRawItem的类，需要实现
                'item_parse_class': BaseItemCommonParser,

                # 其它信息，可以辅助生成CommonRawItem的字段
                # 参考函数parse_list_page_common() 中 item_parser.get_common_raw_item()代码
                'tos': '工程建设',
                'tos_code': '01',
                'source': '江苏省招标投标公共服务平台',
                'notice_type': "招标公告",
                'notice_type_code': '0101',
                'area_code': '32',
                'content_code': '1',
                'site_name': '江苏省招标投标公共服务平台',
                'industry': '工程建设',
                'bid_type': 'TenderBulletin',
                'time_type': 6 if self.crawl_mode == CrawlMode.HISTORY else 0,
            },
            'page_3': {
                # 通常会被填充在'source'字段里，有时也可以放在'tos'
                'name': '江苏省招标投标公共服务平台',

                # list页面的base地址
                'base_url': 'http://api.jszbtb.com/DataSyncApi/HomeWinCandidateBulletin?',

                # list页面的call_back处理函数
                'callback': self.parse_list_page_common,

                'method': "get",

                'requests_type': "dict",

                # 得到下一页url的函数，返回值一定是一个url
                'get_next_page_url': self.get_normal_next_page_url,

                # 网站中该页面的最大页数，（可选配置，仅为优化程序执行效率，可不填）
                'stop_page_num': 1000,

                # 连续遇到[stop_dup_item_num]个重复条目后，停止本次抓取
                # 提示：在程序运行初始阶段，此值可以设的较大，以便爬取所有的历史记录
                'stop_dup_item_num': 500000 if self.crawl_mode == CrawlMode.HISTORY else 60,

                # list页面中，获得条目列表的xpath
                'xpath_of_list': ['data', 'data'],

                # 获得每一个条目链接地址的xpath
                'xpath_of_detail_url': 'id',

                # 对每一个条目进行解析，返回CommonRawItem的类，需要实现
                'item_parse_class': BaseItemCommonParser,

                # 其它信息，可以辅助生成CommonRawItem的字段
                # 参考函数parse_list_page_common() 中 item_parser.get_common_raw_item()代码
                'tos': '工程建设',
                'tos_code': '01',
                'source': '江苏省招标投标公共服务平台',
                'notice_type': "中标候选人公告",
                'notice_type_code': '0104',
                'area_code': '32',
                'content_code': '1',
                'site_name': '江苏省招标投标公共服务平台',
                'industry': '工程建设',
                'bid_type': 'WinCandidateBulletin',
                'time_type': 6 if self.crawl_mode == CrawlMode.HISTORY else 0,
            },
            'page_4': {
                # 通常会被填充在'source'字段里，有时也可以放在'tos'
                'name': '江苏省招标投标公共服务平台',

                # list页面的base地址
                'base_url': 'http://api.jszbtb.com/DataSyncApi/HomeWinBidBulletin?',

                # list页面的call_back处理函数
                'callback': self.parse_list_page_common,

                'method': "get",

                'requests_type': "dict",

                # 得到下一页url的函数，返回值一定是一个url
                'get_next_page_url': self.get_normal_next_page_url,

                # 网站中该页面的最大页数，（可选配置，仅为优化程序执行效率，可不填）
                'stop_page_num': 1000,

                # 连续遇到[stop_dup_item_num]个重复条目后，停止本次抓取
                # 提示：在程序运行初始阶段，此值可以设的较大，以便爬取所有的历史记录
                'stop_dup_item_num': 500000 if self.crawl_mode == CrawlMode.HISTORY else 60,

                # list页面中，获得条目列表的xpath
                'xpath_of_list': ['data', 'data'],

                # 获得每一个条目链接地址的xpath
                'xpath_of_detail_url': 'id',

                # 对每一个条目进行解析，返回CommonRawItem的类，需要实现
                'item_parse_class': BaseItemCommonParser,

                # 其它信息，可以辅助生成CommonRawItem的字段
                # 参考函数parse_list_page_common() 中 item_parser.get_common_raw_item()代码
                'tos': '工程建设',
                'tos_code': '01',
                'source': '江苏省招标投标公共服务平台',
                'notice_type': "中标结果公示",
                'notice_type_code': '0104',
                'area_code': '32',
                'content_code': '1',
                'site_name': '江苏省招标投标公共服务平台',
                'industry': '工程建设',
                'bid_type': 'WinBidBulletin',
                'time_type': 6 if self.crawl_mode == CrawlMode.HISTORY else 0,
            },
        }

        logging.info('start crawling...')

        # 轮询每个类别
        for _k, _v in _source_info.items():

            # 填充爬取的基本信息
            self.crawl_helper.init_crawl_info(_k, _v)

            # 假定每个类别有不超过100000个页面
            for _page_num in range(100000):
                # 轮询公告中的不同list页面
                if self.crawl_helper.get_stop_flag(_k):
                    break

                # 根据获得下一页的函数，得到下一页的URL
                _ext_param = {
                    'bid_type': _v['bid_type'],
                    'start_time': self.start_time,
                    'end_time': self.end_time,
                }
                _request_url = _v['get_next_page_url'](page_index=_page_num, base_url=_v['base_url'],
                                                       ext_param=_ext_param)
                # _request = ""
                # 生成request
                if _v["method"] == "post":
                    payload = {}
                    _request = scrapy.FormRequest(url=_request_url, body=payload, callback=_v['callback'])
                else:
                    _request = scrapy.Request(_request_url, callback=_v['callback'])

                # 如果需要js渲染，需要使用下面的函数
                # _request = SplashRequest(_request_url, callback=_v['callback'], args={'wait': 2})

                # 填充必要的参数
                _request.meta['param'] = _v
                _request.meta['crawl_key'] = _k
                _request.meta['page_index'] = _page_num + 1

                yield _request

            # 单个类别的爬取结束
            self.crawl_helper.stop_crawl_info(_k)

        logging.info('stop crawling...')

    def closed(self, reason):
        if self.mongo_client:
            self.mongo_client.close()

        self.crawl_helper.store_crawl_info_2_db(key=None, status='stopped', comment=reason)
        logging.info('Spider[{}] closed, reason:[{}]'.format(self.name, reason))

    @staticmethod
    def get_normal_next_page_url(page_index, base_url, ext_param):
        _param = {
            'PageSize': '20',
            'CurrentPage': page_index + 1
        }
        return '{}{}'.format(base_url, urlencode(_param, quote_via=quote_plus))

    def parse_list_page_common(self, response):
        """
        通用版list页面解析
        必要条件：
        :param response:
        :return:
        """

        assert 'crawl_key' in response.meta
        assert 'page_index' in response.meta
        assert 'param' in response.meta
        assert 'xpath_of_list' in response.meta['param']
        assert 'xpath_of_detail_url' in response.meta['param']
        assert 'item_parse_class' in response.meta['param']

        list_page_content_md5 = hashlib.md5(response.body).hexdigest()
        logging.info('Get page list url, page:[{}], url:[{}], status:[{}], body md5:[{}]'.format(
            response.meta['page_index'],
            response.url,
            response.status,
            list_page_content_md5))

        logging.info('Crawl info: {}'.format(self.crawl_helper.crawl_info))

        crawl_key = response.meta['crawl_key']

        # 更新状态表记录
        self.crawl_helper.store_crawl_info_2_db(crawl_key, 'active')

        if not self.crawl_helper.should_continue_page_parse(response, crawl_key, list_page_content_md5):
            return

        _item_idx = 0
        if response.meta['param']['requests_type'] == "dict":
            _request = response.text.encode('utf-8')
            _response_data = json.loads(response.text)
            # _dict_xpath = response.meta['param']['xpath_of_list'].split("/")
            # if len(_dict_xpath) > 1:
            for _dictn_num in response.meta['param']["xpath_of_list"]:
                _response_data = _response_data[_dictn_num]
            for selector in _response_data:
                _detail_url = ''
                try:
                    _item_idx += 1
                    _detail_url = 'http://www.jszbtb.com/#/bulletindetail/' + response.meta['param']['bid_type'] + '/' + \
                                  str(selector['id'])
                    # _detail_url = response.urljoin(
                    #     selector[response.meta['param']['xpath_of_detail_url']]
                    # )
                    _unq_id = JyScrapyUtil.get_unique_id(_detail_url)

                    logging.info('Parse item, [{}]-[{}/{}]'.format(crawl_key, _item_idx, response.meta['page_index']))

                    # 检查记录是否已在库中，并做相应的跳出动作
                    loop_break, item_break = self.crawl_helper.should_continue_item_parse(crawl_key, _unq_id)
                    if loop_break:
                        return
                    if item_break:
                        continue

                    # 生成并返回爬取item
                    item_parser = response.meta['param']['item_parse_class'](selector)
                    item = item_parser.get_common_raw_item(
                        _id=_unq_id,
                        detail_url=_detail_url,
                        site=self.site,
                        ext_param=response.meta['param']
                    )

                    # 随机休眠
                    time.sleep(random.randint(50, 100) / 1000.0)

                    # 更新数据库中爬取数量
                    self.crawl_helper.increase_total_item_num(crawl_key)

                    logging_item = item.copy()
                    logging_item["content"] = ""
                    logging.info('item is: {}'.format(logging_item))
                    yield item

                except Exception as e:
                    logging.exception('Handle [{}] failed'.format(_detail_url))
        else:
            for selector in response.xpath(response.meta['param']['xpath_of_list']):
                _detail_url = ''
                try:
                    _item_idx += 1
                    _detail_url = response.urljoin(
                        selector.xpath(response.meta['param']['xpath_of_detail_url']).extract_first())
                    _unq_id = JyScrapyUtil.get_unique_id(_detail_url)

                    logging.info('Parse item, [{}]-[{}/{}]'.format(crawl_key, _item_idx, response.meta['page_index']))

                    # 检查记录是否已在库中，并做相应的跳出动作
                    loop_break, item_break = self.crawl_helper.should_continue_item_parse(crawl_key, _unq_id)
                    if loop_break:
                        return
                    if item_break:
                        continue

                    # 生成并返回爬取item
                    item_parser = response.meta['param']['item_parse_class'](selector)
                    item = item_parser.get_common_raw_item(
                        _id=_unq_id,
                        detail_url=_detail_url,
                        site=self.site,
                        ext_param=response.meta['param']
                    )

                    # 随机休眠
                    time.sleep(random.randint(50, 100) / 1000.0)

                    # 更新数据库中爬取数量
                    self.crawl_helper.increase_total_item_num(crawl_key)

                    logging_item = item.copy()
                    logging_item["content"] = ""
                    logging.info('item is: {}'.format(logging_item))
                    yield item

                except Exception as e:
                    logging.exception('Handle [{}] failed'.format(_detail_url))


class BaseItemCommonParser:
    """
    根据list page页面的每一个条目生成CommonRawItem
    """

    def __init__(self, selector):
        self.selector = selector
        self.item = None

    # 传入参数需要根据具体情况修改
    def get_common_raw_item(self, _id, detail_url, site, ext_param):
        self.item = CommonRawItem()

        # 以下参数必填
        self.item['_id'] = _id
        self.item['site'] = site
        self.item['url'] = detail_url

        # 以下根据网页解析，根据具体情况修改
        self.item['area'] = self.__get_area__()
        self.item['area_detail'] = ''
        self.item['notice_time'] = self.__get_notice_time__()
        self.item['buyer'] = ''
        self.item['title'] = self.__get_title__()
        self.item['content'] = self.__get_content__(detail_url)
        self.item['time_stamp'] = self.__get_time_stamp__()

        # 以下是随参数传递进来的项，根据具体情况修改
        self.item['notice_type'] = ext_param['notice_type']
        self.item['tos'] = ext_param['tos']
        self.item['source'] = ext_param['source']
        self.item['tos_code'] = ext_param['tos_code']
        self.item['notice_type_code'] = ext_param['notice_type_code']
        self.item['area_code'] = ext_param['area_code']
        self.item['content_code'] = ext_param['content_code']
        self.item['site_name'] = ext_param['site_name']
        self.item['industry'] = ext_param['industry']

        return self.item

    def __get_area__(self):
        try:
            _ret = '江苏省'
        except:
            _ret = ''
            logging.exception('[{}] get_area failed'.format(self.item['_id']))

        return _ret

    def __get_area_detail__(self):
        try:
            _ret = ''
        except:
            _ret = ''
            logging.exception('[{}] get_area_detail failed'.format(self.item['_id']))

        return _ret

    def __get_notice_time__(self):
        try:
            # 网页格式: 2020-01-20
            # 必须是以下格式: '2020.01.21 10:00:00'
            _notice_time = self.selector['create_time'].replace('T', ' ').split('.')[0]
            _ret = _notice_time.replace('-', '.')
        except:
            _ret = ''
            logging.exception('[{}] get_notice_time failed'.format(self.item['_id']))

        return _ret

    def __get_buyer__(self):
        try:
            _ret = ''
        except:
            _ret = ''
            logging.exception('[{}] get_buyer failed'.format(self.item['_id']))

        return _ret

    def __get_title__(self):
        """
        正文标题
        如果提取正文标题失败，则判断此次爬取失败，所以这里不能用try except
        :param url:
        :return:
        """
        _ret = self.selector['bulletinName']

        return _ret

    def __get_content__(self, url):
        """
        正文内容
        如果提取正文内容失败，则判断此次爬取失败，所以这里不能用try except
        :param url:
        :return:
        """
        _bad = False
        _ret = ''
        try:
            _r = requests.get(url, verify=False, timeout=15)
            # _r = JyScrapyUtil.request_html_by_proxy(url)
            _r.encoding = 'utf-8'
            _ret = base64.b64encode(zlib.compress(_r.text.encode('utf-8'))).decode('utf-8')
        except:
            _bad = True

        # 如果有异常，重试一次
        if _bad:
            time.sleep(1)
            _r = JyScrapyUtil.request_html_by_proxy(url)
            _r.encoding = 'utf-8'
            _ret = base64.b64encode(zlib.compress(_r.text.encode('utf-8'))).decode('utf-8')

        return _ret

    def __get_time_stamp__(self):
        _ret = 0
        try:
            _ret = int(round(time.time() * 1000, 0))
        except:
            logging.exception('[{}] get_time_stamp failed'.format(self.item['_id']))

        return _ret
