# -*- coding:utf-8 -*-

import json
#import requests
from curl_cffi import requests
from urllib3.util import Retry


class TrendReq(object):
    GET_METHOD = "get"
    POST_METHOD = "post"
    GENERAL_URL = "https://trends.google.com/trends/api/explore"
    INTEREST_OVER_TIME_URL = "https://trends.google.com/trends/api/widgetdata/multiline"


    def __init__(self,hl="en-US",tz=360,geo="",timeout=(2, 5),proxies=None,retries=0,backoff_factor=0):
        self.results = None
        self.tz = tz
        self.hl = hl
        self.geo = geo
        self.kw_list = list()
        self.timeout = timeout
        self.proxies = proxies
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.cookies = self.GetGoogleCookie()
        self.token_payload = dict()
        self.interest_over_time_widget = dict()
        self.interest_by_region_widget = dict()
        self.related_topics_widget_list = list()
        self.related_queries_widget_list = list()


    def GetGoogleCookie(self):
        while True:
            proxy = self.proxies
            print(proxy)
            try:
                return dict(
                    filter(
                        lambda i: i[0] == "NID",
                        requests.get(
                            "https://trends.google.com/?geo={geo}".format(
                                geo=self.hl[-2:]
                            ),
                            timeout=self.timeout,
                            proxies=proxy,
                        ).cookies.items(),
                    )
                )
            except:
                print("Proxy error. Changing IP")
                continue


    def _get_data(self, url, method=GET_METHOD, trim_chars=0, **kwargs):
        s = requests.Session()
        if self.retries > 0 or self.backoff_factor > 0:
            retry = Retry(
                total=self.retries,
                read=self.retries,
                connect=self.retries,
                backoff_factor=self.backoff_factor,
            )

        s.headers.update({"accept-language": self.hl})
        if self.proxies:
            self.cookies = self.GetGoogleCookie()
            s.proxies = self.proxies

        if method == TrendReq.POST_METHOD:
            response = s.post(
                url, timeout=self.timeout, cookies=self.cookies, **kwargs
            )
        else:
            response = s.get(
                url, timeout=self.timeout, cookies=self.cookies, **kwargs
            )
        if (
                response.status_code == 200
                and "application/json" in response.headers["Content-Type"]
                or "application/javascript" in response.headers["Content-Type"]
                or "text/javascript" in response.headers["Content-Type"]
        ):
            content = response.text[trim_chars:]
            return json.loads(content)
        else:
            raise (
                "The request failed: Google returned a "
                "response with code {0}.".format(response.status_code),
            )


    def build_payload(self, kw_list, cat=0, timeframe="today 5-y", geo="", gprop=""):
        self.kw_list = kw_list
        self.geo = geo or self.geo
        self.token_payload = {
            "hl": self.hl,
            "tz": self.tz,
            "req": {"comparisonItem": [], "category": cat, "property": gprop},
        }
        for kw in self.kw_list:
            keyword_payload = {"keyword": kw, "time": timeframe, "geo": self.geo}
            self.token_payload["req"]["comparisonItem"].append(keyword_payload)
        self.token_payload["req"] = json.dumps(self.token_payload["req"])
        self._tokens()
        return


    def _tokens(self):
        widget_dict = self._get_data(
            url=TrendReq.GENERAL_URL,
            method=TrendReq.GET_METHOD,
            params=self.token_payload,
            trim_chars=4,
        )["widgets"]
        first_region_token = True
        self.related_queries_widget_list[:] = []
        self.related_topics_widget_list[:] = []
        for widget in widget_dict:
            if widget["id"] == "TIMESERIES":
                self.interest_over_time_widget = widget
            if widget["id"] == "GEO_MAP" and first_region_token:
                self.interest_by_region_widget = widget
                first_region_token = False
            if "RELATED_TOPICS" in widget["id"]:
                self.related_topics_widget_list.append(widget)
            if "RELATED_QUERIES" in widget["id"]:
                self.related_queries_widget_list.append(widget)
        return


    def interest_over_time(self):
        over_time_payload = {
            "req": json.dumps(self.interest_over_time_widget["request"]),
            "token": self.interest_over_time_widget["token"],
            "tz": self.tz,
        }
        req_json = self._get_data(
            url=TrendReq.INTEREST_OVER_TIME_URL,
            method=TrendReq.GET_METHOD,
            trim_chars=5,
            params=over_time_payload,
        )
        return req_json


def google_index(symbol,start_date: str = "20191201",end_date: str = "20191204"):
    """
    谷歌指数
    :param symbol: 关键词
    :type symbol: str| list
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :return: 谷歌指数
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    pytrends = TrendReq(hl="en-US", tz=360, proxies=proxies)
    if isinstance(symbol,str):
        kw_list = [symbol]
    else:
        kw_list = symbol
    pytrends.build_payload(
        kw_list, cat=0, timeframe=start_date + " " + end_date, geo="", gprop=""
    )
    search_df = pytrends.interest_over_time()
    return search_df


if __name__ == "__main__":
    # 搜索全球范围、所有类别、网页搜索、规定时间的指数
    proxies = {"https": "127.0.0.1:15732"}
    google_index_df = google_index(symbol="lx", start_date="20121122", end_date="20191222")
    print(google_index_df)
    google_index_df = google_index(symbol=["管碧玲","柯呈枋"], start_date="20121122", end_date="20191222")
    print(google_index_df)
