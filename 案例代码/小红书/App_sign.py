# -*- coding: utf-8 -*-

from urllib.parse import quote

'''
APP的sign
'''

def generate_md5(data):
	return hashlib.md5(data.encode("utf-8")).hexdigest()

def get_sign(data):
	keys = list(data.keys())
	keys.sort()
	r1 = "".join([i+"="+data[i] for i in keys])
	r2 = quote(r1)

	deviceId = data["deviceId"].encode("utf-8")
	v1 = ""
	v2 = 0
	for i in r2.encode("utf-8"):
		v1 += str(i ^ deviceId[v2])
		v2 = (v2+1) % len(deviceId)
	r3 = generate_md5(v1)
	sign = generate_md5(r3 + data["deviceId"])
	return sign

params = {
			"page": "1",
			"num": "20",
			"fetch_mode": "1",
			"source": "explore",
			"ads_track_id": "",
			"platform": "android",
			"device_fingerprint": "2019070511014360c1095e3a9c5b2b125182ac4ef9047e01e4b93ed21011a2",
			"device_fingerprint1": "2019070511014360c1095e3a9c5b2b125182ac4ef9047e01e4b93ed21011a2",
			"versionName": "6.6.0",
			"channel": "Xiaomi",
			"sid": "session.1562295755790077877502",
			"lang": "zh-Hans",
			"t": "1563431372",
			"fid": "156335654100d23f4fa1c5ba3929f39cb79289ec3d29",
			"deviceId": "075daade-4c51-3804-8331-c63274c465g7"
			}
print(get_sign(params))

import urllib
import hashlib


def sign_with_query_items(data):
    udid = data['deviceId']
    # 将请求参数按key排序
    data = {k: data[k] for k in sorted(data.keys())}
    # 拼接成字符串
    data_str = ''
    for k, v in data.items():
        data_str += '{}={}'.format(k, v)
    data_str = urllib.parse.quote(data_str, 'utf-8')
    # 将url encode之后的字符串的每个字符与对应的udid字符进行异或原形
    xor_str = ''
    udid_length = len(udid)
    for i in range(len(data_str)):
        data_char = data_str[i]
        udid_index = int(i % udid_length)
        udid_char = udid[udid_index]
        rst = ord(udid_char) ^ ord(data_char)
        xor_str += str(rst)

    # 对异或后的字符串MD5
    md5 = hashlib.md5()
    md5.update(xor_str.encode())
    md5_str = md5.hexdigest()

    # 将MD5后的字符串和udid拼接起来，再次MD5
    md5_str += udid
    md5 = hashlib.md5()
    md5.update(md5_str.encode())
    md5_str = md5.hexdigest()
    return md5_str
print(sign_with_query_items(params))
