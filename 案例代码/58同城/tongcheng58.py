# -*- coding: utf-8 -*-
# @Author  : lx

# 58同城登录
import math, random, time
import requests, re
import execjs

headers = {
    'referer': 'https://passport.58.com/login?path=https%3A%2F%2Fmy.58.com%2F',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
}


def get_token():
    pathtime = str(int(time.time() * 1000))
    jsoncallback = "JsonpCallBack" + str(int(time.time() * 1000)) + str(math.floor(1000.0 * random.random()))
    url = "https://passport.58.com/58/login/init?source=58-homepage-pc&path=https%253A%252F%252Fbj.58.com%252F%253Fpts%253D{}&psdk-d=jsdk&psdk-v=1.0.6&callback=JsonpCallBack{}".format(
        pathtime, jsoncallback)
    doc = requests.get(url, headers=headers).text
    token = re.findall('"token":"(.*?)",', doc)[0]
    return token


def get_pwd(password):
    pwd_script = '''
    window = this;
    function encryptString(pwd) {
        var ii = 1411093327735 - (new Date).getTime();
        var o = (new Date).getTime() + ii;
        var i = o + pwd;
        var r = RSAUtils.getKeyPair("010001", "", "008baf14121377fc76eaf7794b8a8af17085628c3590df47e6534574efcfd81ef8635fcdc67d141c15f51649a89533df0db839331e30b8f8e4440ebf7ccbcc494f4ba18e9f492534b8aafc1b1057429ac851d3d9eb66e86fce1b04527c7b95a2431b07ea277cde2365876e2733325df04389a9d891c5d36b7bc752140db74cb69f");
        return RSAUtils.encryptedString(r, i)
    }

    !function(e) {
        void 0 === e.RSAUtils && (e.RSAUtils = {});
        var s, l, v, c = 16, N = 65536, m = N - 1, M = e.BigInt = function(i) {
            this.digits = "boolean" == typeof i && 1 == i ? null : s.slice(0),
            this.isNeg = !1
        }
        ;
        RSAUtils.setMaxDigits = function(i) {
            s = new Array(i);
            for (var t = 0; t < s.length; t++)
                s[t] = 0;
            l = new M,
            (v = new M).digits[0] = 1
        }
        ,
        RSAUtils.setMaxDigits(20);
        RSAUtils.biFromNumber = function(i) {
            var t = new M;
            t.isNeg = i < 0,
            i = Math.abs(i);
            for (var s = 0; 0 < i; )
                t.digits[s++] = i & m,
                i = Math.floor(i / N);
            return t
        }
        ;
        var g = RSAUtils.biFromNumber(1e15);
        RSAUtils.biFromDecimal = function(i) {
            for (var t, s = "-" == i.charAt(0), r = s ? 1 : 0; r < i.length && "0" == i.charAt(r); )
                ++r;
            if (r == i.length)
                t = new M;
            else {
                var e = (i.length - r) % 15;
                for (0 == e && (e = 15),
                t = RSAUtils.biFromNumber(Number(i.substr(r, e))),
                r += e; r < i.length; )
                    t = RSAUtils.biAdd(RSAUtils.biMultiply(t, g), RSAUtils.biFromNumber(Number(i.substr(r, 15)))),
                    r += 15;
                t.isNeg = s
            }
            return t
        }
        ,
        RSAUtils.biCopy = function(i) {
            var t = new M(!0);
            return t.digits = i.digits.slice(0),
            t.isNeg = i.isNeg,
            t
        }
        ,
        RSAUtils.reverseStr = function(i) {
            for (var t = "", s = i.length - 1; -1 < s; --s)
                t += i.charAt(s);
            return t
        }
        ;
        var n = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"];
        RSAUtils.biToString = function(i, t) {
            var s = new M;
            s.digits[0] = t;
            for (var r = RSAUtils.biDivideModulo(i, s), e = n[r[1].digits[0]]; 1 == RSAUtils.biCompare(r[0], l); )
                r = RSAUtils.biDivideModulo(r[0], s),
                digit = r[1].digits[0],
                e += n[r[1].digits[0]];
            return (i.isNeg ? "-" : "") + RSAUtils.reverseStr(e)
        }
        ,
        RSAUtils.biToDecimal = function(i) {
            var t = new M;
            t.digits[0] = 10;
            for (var s = RSAUtils.biDivideModulo(i, t), r = String(s[1].digits[0]); 1 == RSAUtils.biCompare(s[0], l); )
                s = RSAUtils.biDivideModulo(s[0], t),
                r += String(s[1].digits[0]);
            return (i.isNeg ? "-" : "") + RSAUtils.reverseStr(r)
        }
        ;
        var r = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"];
        RSAUtils.digitToHex = function(t) {
            var s = "";
            for (i = 0; i < 4; ++i)
                s += r[15 & t],
                t >>>= 4;
            return RSAUtils.reverseStr(s)
        }
        ,
        RSAUtils.biToHex = function(i) {
            for (var t = "", s = (RSAUtils.biHighIndex(i),
            RSAUtils.biHighIndex(i)); -1 < s; --s)
                t += RSAUtils.digitToHex(i.digits[s]);
            return t
        }
        ,
        RSAUtils.charToHex = function(i) {
            return 48 <= i && i <= 57 ? i - 48 : 65 <= i && i <= 90 ? 10 + i - 65 : 97 <= i && i <= 122 ? 10 + i - 97 : 0
        }
        ,
        RSAUtils.hexToDigit = function(i) {
            for (var t = 0, s = Math.min(i.length, 4), r = 0; r < s; ++r)
                t <<= 4,
                t |= RSAUtils.charToHex(i.charCodeAt(r));
            return t
        }
        ,
        RSAUtils.biFromHex = function(i) {
            for (var t = new M, s = i.length, r = 0; 0 < s; s -= 4,
            ++r)
                t.digits[r] = RSAUtils.hexToDigit(i.substr(Math.max(s - 4, 0), Math.min(s, 4)));
            return t
        }
        ,
        RSAUtils.biFromString = function(i, t) {
            var s = "-" == i.charAt(0)
              , r = s ? 1 : 0
              , e = new M
              , l = new M;
            l.digits[0] = 1;
            for (var g = i.length - 1; r <= g; g--) {
                var n = i.charCodeAt(g)
                  , d = RSAUtils.charToHex(n)
                  , o = RSAUtils.biMultiplyDigit(l, d);
                e = RSAUtils.biAdd(e, o),
                l = RSAUtils.biMultiplyDigit(l, t)
            }
            return e.isNeg = s,
            e
        }
        ,
        RSAUtils.biDump = function(i) {
            return (i.isNeg ? "-" : "") + i.digits.join(" ")
        }
        ,
        RSAUtils.biAdd = function(i, t) {
            var s;
            if (i.isNeg != t.isNeg)
                t.isNeg = !t.isNeg,
                s = RSAUtils.biSubtract(i, t),
                t.isNeg = !t.isNeg;
            else {
                s = new M;
                for (var r, e = 0, l = 0; l < i.digits.length; ++l)
                    r = i.digits[l] + t.digits[l] + e,
                    s.digits[l] = r % N,
                    e = Number(N <= r);
                s.isNeg = i.isNeg
            }
            return s
        }
        ,
        RSAUtils.biSubtract = function(i, t) {
            var s;
            if (i.isNeg != t.isNeg)
                t.isNeg = !t.isNeg,
                s = RSAUtils.biAdd(i, t),
                t.isNeg = !t.isNeg;
            else {
                var r, e;
                s = new M;
                for (var l = e = 0; l < i.digits.length; ++l)
                    r = i.digits[l] - t.digits[l] + e,
                    s.digits[l] = r % N,
                    s.digits[l] < 0 && (s.digits[l] += N),
                    e = 0 - Number(r < 0);
                if (-1 == e) {
                    for (l = e = 0; l < i.digits.length; ++l)
                        r = 0 - s.digits[l] + e,
                        s.digits[l] = r % N,
                        s.digits[l] < 0 && (s.digits[l] += N),
                        e = 0 - Number(r < 0);
                    s.isNeg = !i.isNeg
                } else
                    s.isNeg = i.isNeg
            }
            return s
        }
        ,
        RSAUtils.biHighIndex = function(i) {
            for (var t = i.digits.length - 1; 0 < t && 0 == i.digits[t]; )
                --t;
            return t
        }
        ,
        RSAUtils.biNumBits = function(i) {
            var t, s = RSAUtils.biHighIndex(i), r = i.digits[s], e = (s + 1) * c;
            for (t = e; e - c < t && 0 == (32768 & r); --t)
                r <<= 1;
            return t
        }
        ,
        RSAUtils.biMultiply = function(i, t) {
            for (var s, r, e, l = new M, g = RSAUtils.biHighIndex(i), n = RSAUtils.biHighIndex(t), d = 0; d <= n; ++d) {
                for (e = d,
                j = s = 0; j <= g; ++j,
                ++e)
                    r = l.digits[e] + i.digits[j] * t.digits[d] + s,
                    l.digits[e] = r & m,
                    s = r >>> 16;
                l.digits[d + g + 1] = s
            }
            return l.isNeg = i.isNeg != t.isNeg,
            l
        }
        ,
        RSAUtils.biMultiplyDigit = function(i, t) {
            var s, r, e;
            result = new M,
            s = RSAUtils.biHighIndex(i);
            for (var l = r = 0; l <= s; ++l)
                e = result.digits[l] + i.digits[l] * t + r,
                result.digits[l] = e & m,
                r = e >>> 16;
            return result.digits[1 + s] = r,
            result
        }
        ,
        RSAUtils.arrayCopy = function(i, t, s, r, e) {
            for (var l = Math.min(t + e, i.length), g = t, n = r; g < l; ++g,
            ++n)
                s[n] = i[g]
        }
        ;
        var d = [0, 32768, 49152, 57344, 61440, 63488, 64512, 65024, 65280, 65408, 65472, 65504, 65520, 65528, 65532, 65534, 65535];
        RSAUtils.biShiftLeft = function(i, t) {
            var s = Math.floor(t / c)
              , r = new M;
            RSAUtils.arrayCopy(i.digits, 0, r.digits, s, r.digits.length - s);
            for (var e = t % c, l = c - e, g = r.digits.length - 1, n = g - 1; 0 < g; --g,
            --n)
                r.digits[g] = r.digits[g] << e & m | (r.digits[n] & d[e]) >>> l;
            return r.digits[0] = r.digits[g] << e & m,
            r.isNeg = i.isNeg,
            r
        }
        ;
        var o = [0, 1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535];
        function u(i) {
            var t = RSAUtils
              , s = t.biDivideByRadixPower(i, this.k - 1)
              , r = t.biMultiply(s, this.mu)
              , e = t.biDivideByRadixPower(r, this.k + 1)
              , l = t.biModuloByRadixPower(i, this.k + 1)
              , g = t.biMultiply(e, this.modulus)
              , n = t.biModuloByRadixPower(g, this.k + 1)
              , d = t.biSubtract(l, n);
            d.isNeg && (d = t.biAdd(d, this.bkplus1));
            for (var o = 0 <= t.biCompare(d, this.modulus); o; )
                d = t.biSubtract(d, this.modulus),
                o = 0 <= t.biCompare(d, this.modulus);
            return d
        }
        function S(i, t) {
            var s = RSAUtils.biMultiply(i, t);
            return this.modulo(s)
        }
        function a(i, t) {
            var s = new M;
            s.digits[0] = 1;
            for (var r = i, e = t; 0 != (1 & e.digits[0]) && (s = this.multiplyMod(s, r)),
            0 != (e = RSAUtils.biShiftRight(e, 1)).digits[0] || 0 != RSAUtils.biHighIndex(e); )
                r = this.multiplyMod(r, r);
            return s
        }
        RSAUtils.biShiftRight = function(i, t) {
            var s = Math.floor(t / c)
              , r = new M;
            RSAUtils.arrayCopy(i.digits, s, r.digits, 0, i.digits.length - s);
            for (var e = t % c, l = c - e, g = 0, n = g + 1; g < r.digits.length - 1; ++g,
            ++n)
                r.digits[g] = r.digits[g] >>> e | (r.digits[n] & o[e]) << l;
            return r.digits[r.digits.length - 1] >>>= e,
            r.isNeg = i.isNeg,
            r
        }
        ,
        RSAUtils.biMultiplyByRadixPower = function(i, t) {
            var s = new M;
            return RSAUtils.arrayCopy(i.digits, 0, s.digits, t, s.digits.length - t),
            s
        }
        ,
        RSAUtils.biDivideByRadixPower = function(i, t) {
            var s = new M;
            return RSAUtils.arrayCopy(i.digits, t, s.digits, 0, s.digits.length - t),
            s
        }
        ,
        RSAUtils.biModuloByRadixPower = function(i, t) {
            var s = new M;
            return RSAUtils.arrayCopy(i.digits, 0, s.digits, 0, t),
            s
        }
        ,
        RSAUtils.biCompare = function(i, t) {
            if (i.isNeg != t.isNeg)
                return 1 - 2 * Number(i.isNeg);
            for (var s = i.digits.length - 1; 0 <= s; --s)
                if (i.digits[s] != t.digits[s])
                    return i.isNeg ? 1 - 2 * Number(i.digits[s] > t.digits[s]) : 1 - 2 * Number(i.digits[s] < t.digits[s]);
            return 0
        }
        ,
        RSAUtils.biDivideModulo = function(i, t) {
            var s, r, e = RSAUtils.biNumBits(i), l = RSAUtils.biNumBits(t), g = t.isNeg;
            if (e < l)
                return i.isNeg ? ((s = RSAUtils.biCopy(v)).isNeg = !t.isNeg,
                i.isNeg = !1,
                t.isNeg = !1,
                r = biSubtract(t, i),
                i.isNeg = !0,
                t.isNeg = g) : (s = new M,
                r = RSAUtils.biCopy(i)),
                [s, r];
            s = new M,
            r = i;
            for (var n = Math.ceil(l / c) - 1, d = 0; t.digits[n] < 32768; )
                t = RSAUtils.biShiftLeft(t, 1),
                ++d,
                ++l,
                n = Math.ceil(l / c) - 1;
            r = RSAUtils.biShiftLeft(r, d),
            e += d;
            for (var o = Math.ceil(e / c) - 1, u = RSAUtils.biMultiplyByRadixPower(t, o - n); -1 != RSAUtils.biCompare(r, u); )
                ++s.digits[o - n],
                r = RSAUtils.biSubtract(r, u);
            for (var S = o; n < S; --S) {
                var a = S >= r.digits.length ? 0 : r.digits[S]
                  , b = S - 1 >= r.digits.length ? 0 : r.digits[S - 1]
                  , A = S - 2 >= r.digits.length ? 0 : r.digits[S - 2]
                  , R = n >= t.digits.length ? 0 : t.digits[n]
                  , h = n - 1 >= t.digits.length ? 0 : t.digits[n - 1];
                s.digits[S - n - 1] = a == R ? m : Math.floor((a * N + b) / R);
                for (var U = s.digits[S - n - 1] * (R * N + h), f = 4294967296 * a + (b * N + A); f < U; )
                    --s.digits[S - n - 1],
                    U = s.digits[S - n - 1] * (R * N | h),
                    f = a * N * N + (b * N + A);
                u = RSAUtils.biMultiplyByRadixPower(t, S - n - 1),
                (r = RSAUtils.biSubtract(r, RSAUtils.biMultiplyDigit(u, s.digits[S - n - 1]))).isNeg && (r = RSAUtils.biAdd(r, u),
                --s.digits[S - n - 1])
            }
            return r = RSAUtils.biShiftRight(r, d),
            s.isNeg = i.isNeg != g,
            i.isNeg && (s = g ? RSAUtils.biAdd(s, v) : RSAUtils.biSubtract(s, v),
            t = RSAUtils.biShiftRight(t, d),
            r = RSAUtils.biSubtract(t, r)),
            0 == r.digits[0] && 0 == RSAUtils.biHighIndex(r) && (r.isNeg = !1),
            [s, r]
        }
        ,
        RSAUtils.biDivide = function(i, t) {
            return RSAUtils.biDivideModulo(i, t)[0]
        }
        ,
        RSAUtils.biModulo = function(i, t) {
            return RSAUtils.biDivideModulo(i, t)[1]
        }
        ,
        RSAUtils.biMultiplyMod = function(i, t, s) {
            return RSAUtils.biModulo(RSAUtils.biMultiply(i, t), s)
        }
        ,
        RSAUtils.biPow = function(i, t) {
            for (var s = v, r = i; 0 != (1 & t) && (s = RSAUtils.biMultiply(s, r)),
            0 != (t >>= 1); )
                r = RSAUtils.biMultiply(r, r);
            return s
        }
        ,
        RSAUtils.biPowMod = function(i, t, s) {
            for (var r = v, e = i, l = t; 0 != (1 & l.digits[0]) && (r = RSAUtils.biMultiplyMod(r, e, s)),
            0 != (l = RSAUtils.biShiftRight(l, 1)).digits[0] || 0 != RSAUtils.biHighIndex(l); )
                e = RSAUtils.biMultiplyMod(e, e, s);
            return r
        }
        ,
        e.BarrettMu = function(i) {
            this.modulus = RSAUtils.biCopy(i),
            this.k = RSAUtils.biHighIndex(this.modulus) + 1;
            var t = new M;
            t.digits[2 * this.k] = 1,
            this.mu = RSAUtils.biDivide(t, this.modulus),
            this.bkplus1 = new M,
            this.bkplus1.digits[this.k + 1] = 1,
            this.modulo = u,
            this.multiplyMod = S,
            this.powMod = a
        }
        ;
        function b(i, t, s) {
            var r = RSAUtils;
            this.e = r.biFromHex(i),
            this.d = r.biFromHex(t),
            this.m = r.biFromHex(s),
            this.chunkSize = 2 * r.biHighIndex(this.m),
            this.radix = 16,
            this.barrett = new e.BarrettMu(this.m)
        }
        RSAUtils.getKeyPair = function(i, t, s) {
            return new b(i,t,s)
        }
        ,
        void 0 === e.twoDigit && (e.twoDigit = function(i) {
            return (i < 10 ? "0" : "") + String(i)
        }
        ),
        RSAUtils.encryptedString = function(i, t) {
            for (var s = [], r = t.length, e = 0; e < r; )
                s[e] = t.charCodeAt(e),
                e++;
            for (; s.length % i.chunkSize != 0; )
                s[e++] = 0;
            var l, g, n, d = s.length, o = "";
            for (e = 0; e < d; e += i.chunkSize) {
                for (n = new M,
                l = 0,
                g = e; g < e + i.chunkSize; ++l)
                    n.digits[l] = s[g++],
                    n.digits[l] += s[g++] << 8;
                var u = i.barrett.powMod(n, i.e);
                o += (16 == i.radix ? RSAUtils.biToHex(u) : RSAUtils.biToString(u, i.radix)) + " "
            }
            return o.substring(0, o.length - 1)
        }
        ,
        RSAUtils.decryptedString = function(i, t) {
            var s, r, e, l = t.split(" "), g = "";
            for (s = 0; s < l.length; ++s) {
                var n;
                for (n = 16 == i.radix ? RSAUtils.biFromHex(l[s]) : RSAUtils.biFromString(l[s], i.radix),
                e = i.barrett.powMod(n, i.d),
                r = 0; r <= RSAUtils.biHighIndex(e); ++r)
                    g += String.fromCharCode(255 & e.digits[r], e.digits[r] >> 8)
            }
            return 0 == g.charCodeAt(g.length - 1) && (g = g.substring(0, g.length - 1)),
            g
        }
        ,
        RSAUtils.setMaxDigits(130)
    }(window);
    '''
    pwd = execjs.compile(pwd_script).call("encryptString", password)
    return pwd


login_url = 'https://passport.58.com/58/login/pc/dologin'

data = {
    'username': '你的账号',
    'password': get_pwd('你的密码'),
    'token': get_token(),
    'source': '58-default-pc',
    'path': 'https%3A%2F%2Fmy.58.com%2F%3Fpts%3D{}'.format(str(int(time.time() * 1000))),
    'domain': '58.com',
    'finger2': 'zh-CN|24|1|8|1920_1080|1920_1040|-480|1|1|1|undefined|1|unknown|Win32|unknown|4|false|false|false|false|false|0_false_false|d41d8cd98f00b204e9800998ecf8427e|dcde05a3c1479a1837d039c0c932f6d2',
    'isremember': 'false',
    'autologin': 'false',
    'isredirect': 'false',
    'psdk-d': 'jsdk',
    'psdk-v': '1.0.6',
    # 'fingerprint': 'Hgby5ObB2hQcRL0PrExSil4CoeCI3MZt',
    'callback': 'SDK_CALLBACK_FUN.successFun',
}
res = requests.post(login_url, headers=headers, data=data)
print(res.headers)

# 博客链接：https://blog.csdn.net/weixin_43582101/article/details/109253299