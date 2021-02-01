# -*- coding: utf-8 -*-
# @Author  : lx
# @IDE ：PyCharm

# 搜狐网模拟登录
# https://blog.csdn.net/weixin_43582101/article/details/109601984

import execjs
import requests
import time

def get_pwd_md5():
    pwd_md5 = '''
    function md5(args) {
        function hex_md5(s) {
            return binl2hex(core_md5(str2binl(s), s.length * chrsz))
        }
        function core_md5(x, len) {
            x[len >> 5] |= 128 << len % 32,
            x[14 + (len + 64 >>> 9 << 4)] = len;
            for (var a = 1732584193, b = -271733879, c = -1732584194, d = 271733878, i = 0; i < x.length; i += 16) {
                var olda = a
                  , oldb = b
                  , oldc = c
                  , oldd = d;
                a = md5_ff(a, b, c, d, x[i + 0], 7, -680876936),
                d = md5_ff(d, a, b, c, x[i + 1], 12, -389564586),
                c = md5_ff(c, d, a, b, x[i + 2], 17, 606105819),
                b = md5_ff(b, c, d, a, x[i + 3], 22, -1044525330),
                a = md5_ff(a, b, c, d, x[i + 4], 7, -176418897),
                d = md5_ff(d, a, b, c, x[i + 5], 12, 1200080426),
                c = md5_ff(c, d, a, b, x[i + 6], 17, -1473231341),
                b = md5_ff(b, c, d, a, x[i + 7], 22, -45705983),
                a = md5_ff(a, b, c, d, x[i + 8], 7, 1770035416),
                d = md5_ff(d, a, b, c, x[i + 9], 12, -1958414417),
                c = md5_ff(c, d, a, b, x[i + 10], 17, -42063),
                b = md5_ff(b, c, d, a, x[i + 11], 22, -1990404162),
                a = md5_ff(a, b, c, d, x[i + 12], 7, 1804603682),
                d = md5_ff(d, a, b, c, x[i + 13], 12, -40341101),
                c = md5_ff(c, d, a, b, x[i + 14], 17, -1502002290),
                b = md5_ff(b, c, d, a, x[i + 15], 22, 1236535329),
                a = md5_gg(a, b, c, d, x[i + 1], 5, -165796510),
                d = md5_gg(d, a, b, c, x[i + 6], 9, -1069501632),
                c = md5_gg(c, d, a, b, x[i + 11], 14, 643717713),
                b = md5_gg(b, c, d, a, x[i + 0], 20, -373897302),
                a = md5_gg(a, b, c, d, x[i + 5], 5, -701558691),
                d = md5_gg(d, a, b, c, x[i + 10], 9, 38016083),
                c = md5_gg(c, d, a, b, x[i + 15], 14, -660478335),
                b = md5_gg(b, c, d, a, x[i + 4], 20, -405537848),
                a = md5_gg(a, b, c, d, x[i + 9], 5, 568446438),
                d = md5_gg(d, a, b, c, x[i + 14], 9, -1019803690),
                c = md5_gg(c, d, a, b, x[i + 3], 14, -187363961),
                b = md5_gg(b, c, d, a, x[i + 8], 20, 1163531501),
                a = md5_gg(a, b, c, d, x[i + 13], 5, -1444681467),
                d = md5_gg(d, a, b, c, x[i + 2], 9, -51403784),
                c = md5_gg(c, d, a, b, x[i + 7], 14, 1735328473),
                b = md5_gg(b, c, d, a, x[i + 12], 20, -1926607734),
                a = md5_hh(a, b, c, d, x[i + 5], 4, -378558),
                d = md5_hh(d, a, b, c, x[i + 8], 11, -2022574463),
                c = md5_hh(c, d, a, b, x[i + 11], 16, 1839030562),
                b = md5_hh(b, c, d, a, x[i + 14], 23, -35309556),
                a = md5_hh(a, b, c, d, x[i + 1], 4, -1530992060),
                d = md5_hh(d, a, b, c, x[i + 4], 11, 1272893353),
                c = md5_hh(c, d, a, b, x[i + 7], 16, -155497632),
                b = md5_hh(b, c, d, a, x[i + 10], 23, -1094730640),
                a = md5_hh(a, b, c, d, x[i + 13], 4, 681279174),
                d = md5_hh(d, a, b, c, x[i + 0], 11, -358537222),
                c = md5_hh(c, d, a, b, x[i + 3], 16, -722521979),
                b = md5_hh(b, c, d, a, x[i + 6], 23, 76029189),
                a = md5_hh(a, b, c, d, x[i + 9], 4, -640364487),
                d = md5_hh(d, a, b, c, x[i + 12], 11, -421815835),
                c = md5_hh(c, d, a, b, x[i + 15], 16, 530742520),
                b = md5_hh(b, c, d, a, x[i + 2], 23, -995338651),
                a = md5_ii(a, b, c, d, x[i + 0], 6, -198630844),
                d = md5_ii(d, a, b, c, x[i + 7], 10, 1126891415),
                c = md5_ii(c, d, a, b, x[i + 14], 15, -1416354905),
                b = md5_ii(b, c, d, a, x[i + 5], 21, -57434055),
                a = md5_ii(a, b, c, d, x[i + 12], 6, 1700485571),
                d = md5_ii(d, a, b, c, x[i + 3], 10, -1894986606),
                c = md5_ii(c, d, a, b, x[i + 10], 15, -1051523),
                b = md5_ii(b, c, d, a, x[i + 1], 21, -2054922799),
                a = md5_ii(a, b, c, d, x[i + 8], 6, 1873313359),
                d = md5_ii(d, a, b, c, x[i + 15], 10, -30611744),
                c = md5_ii(c, d, a, b, x[i + 6], 15, -1560198380),
                b = md5_ii(b, c, d, a, x[i + 13], 21, 1309151649),
                a = md5_ii(a, b, c, d, x[i + 4], 6, -145523070),
                d = md5_ii(d, a, b, c, x[i + 11], 10, -1120210379),
                c = md5_ii(c, d, a, b, x[i + 2], 15, 718787259),
                b = md5_ii(b, c, d, a, x[i + 9], 21, -343485551),
                a = safe_add(a, olda),
                b = safe_add(b, oldb),
                c = safe_add(c, oldc),
                d = safe_add(d, oldd)
            }
            return Array(a, b, c, d)
        }
        function md5_cmn(q, a, b, x, s, t) {
            return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s), b)
        }
        function md5_ff(a, b, c, d, x, s, t) {
            return md5_cmn(b & c | ~b & d, a, b, x, s, t)
        }
        function md5_gg(a, b, c, d, x, s, t) {
            return md5_cmn(b & d | c & ~d, a, b, x, s, t)
        }
        function md5_hh(a, b, c, d, x, s, t) {
            return md5_cmn(b ^ c ^ d, a, b, x, s, t)
        }
        function md5_ii(a, b, c, d, x, s, t) {
            return md5_cmn(c ^ (b | ~d), a, b, x, s, t)
        }
        function safe_add(x, y) {
            var lsw = (65535 & x) + (65535 & y);
            return (x >> 16) + (y >> 16) + (lsw >> 16) << 16 | 65535 & lsw
        }
        function bit_rol(num, cnt) {
            return num << cnt | num >>> 32 - cnt
        }
        function str2binl(str) {
            for (var bin = Array(), mask = (1 << chrsz) - 1, i = 0; i < str.length * chrsz; i += chrsz)
                bin[i >> 5] |= (str.charCodeAt(i / chrsz) & mask) << i % 32;
            return bin
        }
        function binl2hex(binarray) {
            for (var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef", str = "", i = 0; i < 4 * binarray.length; i++)
                str += hex_tab.charAt(binarray[i >> 2] >> i % 4 * 8 + 4 & 15) + hex_tab.charAt(binarray[i >> 2] >> i % 4 * 8 & 15);
            return str
        }
        var hexcase = 0
          , chrsz = 8;
        return hex_md5(args)
    }
    '''
    result = execjs.compile(pwd_md5).call("md5",password)
    return result


headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'content-length': '136',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.sohu.com',
        'referer': 'https://www.sohu.com/',
        'sec-fetch-dest': 'iframe',
        'cookie':'cookie: SUV=201010154644MXMW; gidinf=x099980109ee123f3b3ab2469000e2ef7c5189f4e0d1; IPLOC=CN; reqtype=pc; BAIDU_SSP_lcr=https://www.baidu.com/link?url=ij36mi7Uep7D8BP9gPfQk6D6kCh2dAJocULa-VdL81S&wd=&eqid=c2b4d2990000f9ab000000035faa5186; _sgid=_SSA.d60beb68b47bcc1bb7ad2a9964a5ab9e; access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1aXMiLCJibGVuZF9pZCI6Ik1ESmhPR0poWWpKbU5UQXlNVEF3TUE9PS5NVE15TmpBNU5UZzFNelV6T0RNek5qYzJPRUJ6YjJoMUxtTnZiUT09IiwiaWF0IjoxNjA1MDAxMzY5fQ.KkXlUTdp1oUbpZRVLHh3tDod90Af_2mfXTrma0aU_Yc; user_id=02a8bab2f5021000; t=1605001416491; jv=c0ff0f5a1857392e7764fdd1d3fe1596-5Kily6iS1605001435022',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        }

login_url = "https://v4.passport.sohu.com/i/login/116005"
username = "你的账号"
password = '你的密码'
data = {
    "userid": username,
    "password": get_pwd_md5(),
    "persistentCookie": "1",
    "appid": "116005",
    "callback": "passport403_cb" + str(int(time.time() * 1000))
}
doc = requests.post(login_url,data=data,headers=headers).text
print(doc)

