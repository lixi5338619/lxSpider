import json
import requests
import execjs
from lxpy import copy_headers_dict

sha1 = 'e7d2753d55876f89967727e909d7bcbdf36653a8be2c5f9f57789fec4d4284ed'
url = f"https://www.virustotal.com/ui/search?limit=20&relationships%5Bcomment%5D=author%2Citem&query={sha1}"

headers = copy_headers_dict('''
    authority: www.virustotal.com
    method: GET
    path: /ui/search?limit=20&relationships%5Bcomment%5D=author%2Citem&query=e7d2753d55876f89967727e909d7bcbdf36653a8be2c5f9f57789fec4d4284ed
    scheme: https
    accept: application/json
    accept-encoding: gzip, deflate, br
    accept-ianguage: en-US,en;q=0.9,es;q=0.8
    accept-language: zh-CN,zh;q=0.9
    content-type: application/json
    cookie: _ga=GA1.2.1266770617.1625465446; _gid=GA1.2.10603261.1625465446; _gat=1
    referer: https://www.virustotal.com/
    sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
    sec-ch-ua-mobile: ?0
    sec-fetch-dest: empty
    sec-fetch-mode: cors
    sec-fetch-site: same-origin
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
    x-app-version: v1x28x5
    x-tool: vt-ui-main
''')

js = '''
function get_anti(){
            const e = Date.now() / 1e3;
             return Buffer.from((`${(()=>{
                const e = 1e10 * (1 + Math.random() % 5e4);
                return e < 50 ? "-1" : e.toFixed(0)
            }
            )()}-ZG9udCBiZSBldmls-${e}`)).toString('base64');
        }
'''
xvt_anti = execjs.compile(js).call('get_anti')
headers.update({'x-vt-anti-abuse-header':xvt_anti})
res = requests.get(url=url,headers=headers)
print(res.json())
