import requests

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat'
referer = 'https://servicewechat.com/wx79a83b1a1e8a7978/591/page-frame.html'
cookie = '复制抓包的cookie'


headers = {
    'Host': 'wxmini-api.uyouqu.com',
    #'referer':referer,
    'User-Agent':user_agent,
    'cookie':cookie
}


def search_user(keyword):
    url = 'https://wxmini-api.uyouqu.com/rest/wd/wechatApp/search/user?'
    data = {
        "keyword": keyword,
        "pcursor": "",
        "ussid": ""
    }
    return requests.post(url, headers=headers, json=data).text

def search_video(keyword):
    url = 'https://wxmini-api.uyouqu.com/rest/wd/wechatApp/search/feed?'
    data = {
        "keyword": keyword,
        "pcursor": "",
        "ussid": "",
        "pageSource": 1

    }
    return requests.post(url, headers=headers, json=data).text

def video_info():
    url = 'https://wxmini-api.uyouqu.com/rest/wd/wechatApp/photo/info?'
    data = {
        "kpn": "WECHAT_SMALL_APP",
        "photoId": "5254293468891588895",
        "authorId": "1346454001",
        "usePrefetch": True,
        "pageType": 1,
        "pageSource": 3
    }
    return requests.post(url, headers=headers, json=data).text

def video_comment():
    url = 'https://wxmini-api.uyouqu.com/rest/wd/wechatApp/photo/comment/list?'
    data = {
        "photoId": "5254293468891588895",
        "count": 20
    }
    return requests.post(url, headers=headers, json=data).text

def user_profile():
    url = 'https://wxmini-api.uyouqu.com/rest/wd/wechatApp/user/profile?'
    data = {
        "eid": "1084678836"
    }
    return requests.post(url, headers=headers, json=data).text




print(search_video('lx'))
