# encoding: utf-8

import json
import requests
import execjs

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://bj.ke.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://bj.ke.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

data = '{"service":"https://ajax.api.ke.com/login/login/getuserinfo","version":"2.0"}'

response = requests.post('https://clogin.ke.com/authentication/initialize', headers=headers, data=data)

loginTicketId = response.json().get('loginTicketId')
publicKey = response.json().get('publicKey').get('key')

with open('encrypt.js', encoding='utf8') as r:
    js_str = r.read()
password = execjs.compile(js_str).call('password','12345qwerasdf')
data = {
    'accountSystem': "customer",
    'context': {},
    'credential': {
        'encodeVersion': "2",
        'password': f'{password}',
        'username': '15596870129',
    },
    'loginTicketId': f'{loginTicketId}',
    'mainAuthMethodName': "username-password",
    'service': "https://ajax.api.ke.com/login/login/getuserinfo",
    'srcId': "eyJ0Ijoie1wiZGF0YVwiOlwiNTY1M2U3MTY0MDc4ZGI3NmVkZjQ1MDUxNmZmNDBmYThkMDlhYzM1MjBhYmEyMzBlYWE1YThmYmU3MjczODJhYjU0MjNiY2ZjNjRjZTg0N2EzMTdkNjQ5MDNlMGQ1N2U5MGE1MTMwOWJjOTdiMTE3ZTk4NDdhZjhmYTA4M2M3ZWJiNWZiNzExZTE3ODcwOTNmN2Q4ZGU1ZjRmOTY2MjI5Y2RiN2MyY2RhYzBhMjJlNDU3ZGY5NGVjMzdjMzNkY2Y3NjJkOTliNDc4ZDI0ZDViY2FhYzcxNmFiNmVkY2IyODk3ZWQwMjQwYzVkMGRmMzIwMTg4ZGZlYmE3YzJmNzI3YWQzYTQ2YjdhNDc0YjQ5ZDAxNWRmOTU4MDVlZTdmZmRlOTI4OGVjYTllNTI1YWE0MjZhZDEwMTNmYzk2NmNhYjdlOGMyMTNkMzNiYzA1MzcwMjA5NDgxY2VjMjU3YWVkNVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI3ZWQzMWNmNlwifSIsInIiOiJodHRwczovL2JqLmtlLmNvbS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==",
    'ticketMaxAge': 604800,
    'version': "2.0"
}

response = requests.post('https://clogin.ke.com/authentication/authenticate', headers=headers, data=json.dumps(data))
print(response.text)