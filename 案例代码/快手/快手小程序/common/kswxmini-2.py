import json
import requests
import subprocess

url = 'https://wxmini-api.uyouqu.com/rest/wd/wechatApp/feed/recommend?__NS_sig3='

did = "wxo_lxisagoodmen7e9e1b99bf26184ad96f"

headers={
    "Host": "wxmini-api.uyouqu.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.3 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 wechatdevtools/1.05.2111300 MicroMessenger/8.0.5 Language/zh_CN webview/",
    "content-type": "application/json",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/undefined/devtools/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "cookie": f"sid=kuaishou.wechat.app; appId=ks_wechat_small_app_2; clientid=13; client_key=f60ac815; kpn=WECHAT_SMALL_APP; kpf=OUTSIDE_IOS_H5; mod=iPhone(14); sys=iOS%2010.0.1; wechatVersion=8.0.5; language=zh_CN; brand=devtools; smallAppVersion=; did={did}; nickName=WITHOUT_PERMISSION"
}

data={
	"count": 10,
	"portal": 1,
	"pageType": 2,
	"extraRequestInfo": "{\"scene\":1001,\"fid\":\"\",\"sharerUserId\":\"\",\"curPhotoIndex\":0,\"adShow\":true,\"weChatAd\":{},\"headurl\":\"https://js2.a.kwimgs.com/udata/pkg/fe/profiel_icon_photo_normal@3x.fb3ec1af.png\",\"page\":0}",
	"needLivestream": True,
	"pcursor": 0,
	"sourceFrom": 2
}



data_str = json.dumps(data,separators=(",", ":"))
args = 'appId=ks_wechat_small_app_2clientid=13did='+did+data_str
process = subprocess.Popen(['node', './get_sig3.js',args] ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
sig3 = str(process.stdout.read()).replace('\n','')
print(sig3)
new_url = url+sig3
print(requests.post(new_url, headers=headers, data=json.dumps(data, separators=(",", ":"))).text)
