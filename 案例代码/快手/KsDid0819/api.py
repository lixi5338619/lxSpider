import json
from req import post, request_get_videos,request_get_homes

# 获取个人所有视频
def get_all_videos(user_id, author_name,did):
    res = post(request_get_videos(user_id),did=did)
    feeds = json.loads(res)['data']['visionProfilePhotoList']['feeds']
    short_videos = {}
    for feed in feeds:
        short_videos[feed['photo']['id']] = {
            "timestamp": feed['photo']['timestamp'],
            "author": author_name,
            "download": feed['photo']['photoUrls'][0]['url']
            }
    return short_videos


# 获取主页信息
def get_home_page(kid,did):
    res = post(request_get_homes(kid),did)
    print(res)