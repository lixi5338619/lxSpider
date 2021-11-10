import requests
import execjs

if __name__ == '__main__':
    cookies = {
        'JSESSIONID': '3E18207E60F7236E0D84ED3E9FFDB216',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.cnpcbidding.com/html/1/index.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    response = requests.get('https://www.cnpcbidding.com/cms/pmsbidInfo/homePage', headers=headers,
                            cookies=cookies).json()
    encrypted = response.get('encrypted')
    requestData = response.get('requestData')
    with open('encrypt.js', encoding='utf-8') as r:
        js_str = r.read()
    requestData = execjs.compile(js_str).call('Decrypt', requestData, encrypted)
    print(requestData)
