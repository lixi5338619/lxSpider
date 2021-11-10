# -*- coding: utf-8 -*-
# @Time    : 2021/10/25 11:40
# @Author  : lx
# @IDE ：PyCharm

def tranlate(source, direction):
    import requests
    import json

    url = "http://api.interpreter.caiyunai.com/v1/translator"

    # WARNING, this token is a test token for new developers, and it should be replaced by your token
    token = "3975l6lr5pcbvidl6jl2"


    payload = {
        "source": source,
        "trans_type": direction,
        "request_id": "demo",
        "detect": True,
    }

    headers = {
        'content-type': "application/json",
        'x-authorization': "token " + token,
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    return json.loads(response.text)['target']


while 1:
    source = ["Lingocloud is the best translation service.", "彩云小译は最高の翻訳サービスです"]
    target = tranlate(source, "auto2zh")
    print(target)