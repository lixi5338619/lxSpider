import hashlib
import logging
import requests


class JyScrapyUtil():

    @classmethod
    def get_unique_id(cls, plain_text):
        return hashlib.md5(plain_text.encode('utf-8')).hexdigest()

    @classmethod
    def is_record_in_mongo(cls, _id, mongo_collection_obj):
        ret = False
        try:
            if _id and mongo_collection_obj:
                ret = (mongo_collection_obj.find_one({'_id': _id}, {'_id': 1}) is not None)
        except Exception as e:
            logging.exception('is_record_in_mongo failed')
            pass
        
        return ret

    @classmethod
    def request_rendered_html(cls, org_url, splash_url=None):
        if splash_url is None:
            splash_url = 'http://192.168.100.120:8050'
        render_url = '{}/render.html?url={}'.format(splash_url, org_url)
        return requests.get(render_url, timeout=10)

    @classmethod
    def request_html_by_proxy(cls, url, proxy_srv=None):
        """
        通过代理执行HTTP GET
        代理使用方法：https://github.com/jhao104/proxy_pool
        :param url:
        :param proxy_srv:
        :return: requests.get()
        """
        if proxy_srv is None:
            proxy_srv = 'http://192.168.100.120:5010'

        retry_count = 5
        while retry_count > 0:
            try:
                proxy = requests.get("{}/get/".format(proxy_srv)).json().get("proxy")
                # 使用代理访问
                r = requests.get(url, proxies={"http": "http://{}".format(proxy)}, timeout=15)
                logging.info('Got url[{}] content using proxy:[{}]'.format(url, proxy))
                return r
            except Exception:
                # logging.exception('request_html_by_proxy failed')
                retry_count -= 1

        logging.warning('Get html by proxy failed, please double check proxy srv [{}]'.format(proxy_srv))
        return requests.get(url, timeout=10)

    @classmethod
    def get_http_proxy(cls):
        try:
            proxy_srv = 'http://192.168.100.120:5010'
            proxy = requests.get("{}/get/".format(proxy_srv)).json().get("proxy")
            return "http://{}".format(proxy)
        except:
            pass

        return None
