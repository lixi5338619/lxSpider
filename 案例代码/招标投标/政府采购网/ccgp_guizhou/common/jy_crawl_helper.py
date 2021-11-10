import hashlib
import logging
import requests
import time
from datetime import datetime
from common.jy_utils import JyScrapyUtil


class JyCrawlHelper:

    def __init__(self, spider_name, mongo_client, db_name, col_name):
        self.crawl_info = {}

        self.spider_name = spider_name

        self.mongo_client = mongo_client
        self.mongo_col_obj = self.mongo_client[db_name][col_name]
        self.mongo_stat_obj = self.mongo_client['db_system']['t_spider_status']

        self.STOP_DUP_ITEM = 50
        self.STOP_FAILED_PAGE = 10

    def store_crawl_info_2_db(self, key, status, comment=None):

        update_time = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        if key in self.crawl_info:
            v = self.crawl_info[key]
            id_str = '{}_{}'.format(self.spider_name, key)
            db_item = {
                '_id': hashlib.md5(id_str.encode('utf-8')).hexdigest(),
                'name': self.spider_name,
                'sub_name': key,
                'req_start_time': v['start_time'] if 'start_time' in v else '',
                'req_end_time': v['end_time'] if 'end_time' in v else '',
                'req_start_page': v['start_page'] if 'start_page' in v else '',
                'req_end_page': v['end_page'] if 'end_page' in v else '',
                'req_stop_item': v['stop_item'] if 'stop_item' in v else '',
                'crawl_start_time': v['crawl_start_time'],
                'crawl_end_time': v['crawl_end_time'],
                'crawl_page_num': v['total_page_num'],
                'crawl_item_num': v['total_item_num'],
                'status': status,
                'update_time': update_time,
                'comment': ''
            }
            self.mongo_stat_obj.save(db_item)
        elif key is None:
            for k,v in self.crawl_info.items():
                id_str = '{}_{}'.format(self.spider_name, k)
                self.mongo_stat_obj.update_one({
                    '_id': hashlib.md5(id_str.encode('utf-8')).hexdigest()
                }, {
                    '$set': {
                        'status': status,
                        'update_time': update_time,
                        'comment': comment
                    }
                }, upsert=False)

    def init_crawl_info(self, key, value):
        self.crawl_info[key] = {
            'stop_parse': False,
            'duplicate_records_num': 0,
            'failed_page_num': 0,
            'duplicate_list_page_num': 0,
            'last_list_page_md5': '',
            'total_page_num': 0,
            'total_item_num': 0,
            'stop_page_num': 1000000,
            'stop_dup_item_num': self.STOP_DUP_ITEM,
            'stop_failed_page_num': self.STOP_FAILED_PAGE,

            'crawl_start_time': datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"),
            'crawl_end_time': '',
        }

        if 'stop_page_num' in value:
            self.crawl_info[key]['stop_page_num'] = value['stop_page_num']

        if 'stop_failed_page_num' in value:
            self.crawl_info[key]['stop_failed_page_num'] = value['stop_failed_page_num']

        if 'stop_dup_item_num' in value:
            self.crawl_info[key]['stop_dup_item_num'] = value['stop_dup_item_num']

    def increase_duplicate_page_num(self, key):
        self.crawl_info[key]['duplicate_list_page_num'] += 1

    def increase_duplicate_item_num(self, key):
        self.crawl_info[key]['duplicate_records_num'] += 1

    def increase_failed_page_num(self, key):
        self.crawl_info[key]['failed_page_num'] += 1

    def increase_total_page_num(self, key):
        self.crawl_info[key]['total_page_num'] += 1

    def increase_total_item_num(self, key):
        self.crawl_info[key]['total_item_num'] += 1

    def get_duplicate_item_num(self, key):
        return self.crawl_info[key]['duplicate_records_num']

    def set_duplicate_item_num(self, key, num):
        self.crawl_info[key]['duplicate_records_num'] = num

    def get_duplicate_page_num(self, key):
        return self.crawl_info[key]['duplicate_list_page_num']

    def set_duplicate_page_num(self, key, num):
        self.crawl_info[key]['duplicate_list_page_num'] = num

    def get_failed_page_num(self, key):
        return int(self.crawl_info[key]['failed_page_num'])

    def set_failed_page_num(self, key, num):
        self.crawl_info[key]['failed_page_num'] = num

    def get_stop_failed_page_num(self, key):
        return int(self.crawl_info[key]['stop_failed_page_num'])

    def set_stop_failed_page_num(self, key, num):
        self.crawl_info[key]['stop_failed_page_num'] = num

    def get_total_page_num(self, key):
        return int(self.crawl_info[key]['total_page_num'])

    def get_stop_page_num(self, key):
        return int(self.crawl_info[key]['stop_page_num'])

    def get_last_page_md5(self, key):
        return self.crawl_info[key]['last_list_page_md5']

    def set_last_page_md5(self, key, content_md5):
        self.crawl_info[key]['last_list_page_md5'] = content_md5

    def get_stop_flag(self, key):
        return self.crawl_info[key]['stop_parse']

    def set_stop_flag(self, key):
        self.crawl_info[key]['stop_parse'] = True

    def get_stop_dup_item_num(self, key):
        return self.crawl_info[key]['stop_dup_item_num']

    def stop_crawl_info(self, key):
        self.crawl_info[key]['crawl_end_time'] = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"),

    def should_continue_page_parse(self, response, key, page_content_md5):
        """
        根据HTTP status code判断是否需要进行页面解析，同时存储页面状态
        :param response:
        :param key:
        :param page_content_md5:
        :return:
        """
        try:
            self.increase_total_page_num(key)

            # 如果超过了预设的爬取页面数量，停止爬取
            if self.get_total_page_num(key) > self.get_stop_page_num(key):
                logging.warning('[{}]超过了预设的爬取页面数，停止爬取'.format(key))
                self.set_stop_flag(key)
                return False

            # 如果连续爬取的list page都是一样的内容，停止爬取
            if page_content_md5 == self.get_last_page_md5(key):
                self.increase_duplicate_page_num(key)
            else:
                self.set_last_page_md5(key, page_content_md5)
                self.set_duplicate_page_num(key, 0)
            if self.get_duplicate_page_num(key) > self.get_stop_failed_page_num(key):
                logging.warning('[{}]列表页连续相同内容，停止爬取'.format(key))
                self.set_stop_flag(key)
                return False

            # 如果爬取页面连续失败，停止爬取
            if response.status != 200:
                self.increase_failed_page_num(key)
                if self.get_failed_page_num(key) > self.get_stop_failed_page_num(key):
                    logging.warning('[{}]请求列表页连续失败，停止爬取'.format(key))
                    self.set_stop_flag(key)
                return False
            else:
                self.set_failed_page_num(key, 0)
        except Exception as  e:
            logging.exception('should_continue_page_parse failed')

        return True

    def should_continue_item_parse(self, key, item_id):
        """
        根据item_id判断是否需要进行item存储，同时记录item状态
        :param key:
        :param item_id:
        :return loop_break: 是否要跳出外层的for循环; item_break：是否要忽略本item
        """
        loop_break, item_break = False, False
        if JyScrapyUtil.is_record_in_mongo(item_id, self.mongo_col_obj):
            logging.info('Duplicate item:[{}] total:[{}-{}]'.format(item_id, key, self.get_duplicate_item_num(key)))
            self.increase_duplicate_item_num(key)

            # 如果连续n条重复数据，认为本次爬取已可以结束
            if self.get_duplicate_item_num(key) >= self.get_stop_dup_item_num(key):
                logging.warning('duplicate items[{}-{}] reach limit, stop crawl'.format(
                    key,
                    self.get_duplicate_item_num(key)))
                self.set_stop_flag(key)
                loop_break = True

            item_break = True
        else:
            self.set_duplicate_item_num(key, 0)

        return loop_break, item_break


