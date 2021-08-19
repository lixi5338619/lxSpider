import requests
from lxpy import copy_headers_dict

KuaiShouGraphQL = "https://www.kuaishou.com/graphql"
KuaiShouShortVideos = "https://www.kuaishou.com/short-video/"

def get_headers(did,referer=False):
    diy_head = copy_headers_dict(f'''
    content-type: application/json
    Host: www.kuaishou.com
    Origin: https://www.kuaishou.com
    Pragma: no-cache
    Referer: https://www.kuaishou.com/brilliant
    sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
    sec-ch-ua-mobile: ?0
    Sec-Fetch-Dest: empty
    Sec-Fetch-Mode: cors
    Sec-Fetch-Site: same-origin
    Cookie: kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did={did};
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
    ''')
    if referer:
        diy_head.update({'Referer':referer})
    return diy_head


def get(url, did,referer=True):
    link = KuaiShouShortVideos + url
    if referer:
        diy_head = get_headers(did,link)
    else:
        diy_head = get_headers(did)

    return requests.get(url=link, headers=diy_head, allow_redirects=False).text


def post(js,did):
    response = requests.post(url=KuaiShouGraphQL, json=js, headers=get_headers(did))
    response.encoding = 'utf-8'
    return response.text



def request_get_homes(userId):
    return {
        "operationName": "visionProfile",
        "query": "query visionProfile($userId: String) {  visionProfile(userId: $userId) {    result    hostName    "
                 "userProfile {      ownerCount {        fan        photo        follow        photo_public        "
                 "__typename      }      profile {        gender        user_name        user_id        headurl       "
                 " user_text        user_profile_bg_url        __typename      }      isFollowing      __typename    "
                 "}    __typename  }} ",
        "variables": {
            "userId": userId
        }
    }


def request_get_videos(userId):
    return {
        "operationName": "visionProfilePhotoList",
        "variables": {
            "userId": userId,
            "pcursor": "",
            "page": "profile"
        },
        "query": "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: "
                 "String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: "
                 "$webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n  "
                 "      id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n "
                 "         url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        "
                 "type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n "
                 "  caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n        "
                 "  cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n         "
                 " url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        "
                 "expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      "
                 "}\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n  "
                 "  hostName\n    pcursor\n    __typename\n  }\n}\n "
    }




