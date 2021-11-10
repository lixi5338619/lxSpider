# -*- coding: utf-8 -*-
import json,execjs
import requests
import random
import re
from urllib.parse import quote
import urllib3

DEFAULT_SERVICE_URLS = ('translate.google.ac', 'translate.google.ad', 'translate.google.ae',
                        'translate.google.al', 'translate.google.am', 'translate.google.as',
                        'translate.google.at', 'translate.google.az', 'translate.google.ba',
                        'translate.google.be', 'translate.google.bf', 'translate.google.bg',
                        'translate.google.bi', 'translate.google.bj', 'translate.google.bs',
                        'translate.google.bt', 'translate.google.by', 'translate.google.ca',
                        'translate.google.cat', 'translate.google.cc', 'translate.google.cd',
                        'translate.google.cf', 'translate.google.cg', 'translate.google.ch',
                        'translate.google.ci', 'translate.google.cl', 'translate.google.cm',
                        'translate.google.cn', 'translate.google.co.ao', 'translate.google.co.bw',
                        'translate.google.co.ck', 'translate.google.co.cr', 'translate.google.co.id',
                        'translate.google.co.il', 'translate.google.co.in', 'translate.google.co.jp',
                        'translate.google.co.ke', 'translate.google.co.kr', 'translate.google.co.ls',
                        'translate.google.co.ma', 'translate.google.co.mz', 'translate.google.co.nz',
                        'translate.google.co.th', 'translate.google.co.tz', 'translate.google.co.ug',
                        'translate.google.co.uk', 'translate.google.co.uz', 'translate.google.co.ve',
                        'translate.google.co.vi', 'translate.google.co.za', 'translate.google.co.zm',
                        'translate.google.co.zw', 'translate.google.co', 'translate.google.com.af',
                        'translate.google.com.ag', 'translate.google.com.ai', 'translate.google.com.ar',
                        'translate.google.com.au', 'translate.google.com.bd', 'translate.google.com.bh',
                        'translate.google.com.bn', 'translate.google.com.bo', 'translate.google.com.br',
                        'translate.google.com.bz', 'translate.google.com.co', 'translate.google.com.cu',
                        'translate.google.com.cy', 'translate.google.com.do', 'translate.google.com.ec',
                        'translate.google.com.eg', 'translate.google.com.et', 'translate.google.com.fj',
                        'translate.google.com.gh', 'translate.google.com.gi', 'translate.google.com.gt',
                        'translate.google.com.hk', 'translate.google.com.jm', 'translate.google.com.kh',
                        'translate.google.com.kw', 'translate.google.com.lb', 'translate.google.com.lc',
                        'translate.google.com.ly', 'translate.google.com.mm', 'translate.google.com.mt',
                        'translate.google.com.mx', 'translate.google.com.my', 'translate.google.com.na',
                        'translate.google.com.ng', 'translate.google.com.ni', 'translate.google.com.np',
                        'translate.google.com.om', 'translate.google.com.pa', 'translate.google.com.pe',
                        'translate.google.com.pg', 'translate.google.com.ph', 'translate.google.com.pk',
                        'translate.google.com.pr', 'translate.google.com.py', 'translate.google.com.qa',
                        'translate.google.com.sa', 'translate.google.com.sb', 'translate.google.com.sg',
                        'translate.google.com.sl', 'translate.google.com.sv', 'translate.google.com.tj',
                        'translate.google.com.tr', 'translate.google.com.tw', 'translate.google.com.ua',
                        'translate.google.com.uy', 'translate.google.com.vc', 'translate.google.com.vn',
                        'translate.google.com', 'translate.google.cv', 'translate.google.cx',
                        'translate.google.cz', 'translate.google.de', 'translate.google.dj',
                        'translate.google.dk', 'translate.google.dm', 'translate.google.dz',
                        'translate.google.ee', 'translate.google.es', 'translate.google.eu',
                        'translate.google.fi', 'translate.google.fm', 'translate.google.fr',
                        'translate.google.ga', 'translate.google.ge', 'translate.google.gf',
                        'translate.google.gg', 'translate.google.gl', 'translate.google.gm',
                        'translate.google.gp', 'translate.google.gr', 'translate.google.gy',
                        'translate.google.hn', 'translate.google.hr', 'translate.google.ht',
                        'translate.google.hu', 'translate.google.ie', 'translate.google.im',
                        'translate.google.io', 'translate.google.iq', 'translate.google.is',
                        'translate.google.it', 'translate.google.je', 'translate.google.jo',
                        'translate.google.kg', 'translate.google.ki', 'translate.google.kz',
                        'translate.google.la', 'translate.google.li', 'translate.google.lk',
                        'translate.google.lt', 'translate.google.lu', 'translate.google.lv',
                        'translate.google.md', 'translate.google.me', 'translate.google.mg',
                        'translate.google.mk', 'translate.google.ml', 'translate.google.mn',
                        'translate.google.ms', 'translate.google.mu', 'translate.google.mv',
                        'translate.google.mw', 'translate.google.ne', 'translate.google.nf',
                        'translate.google.nl', 'translate.google.no', 'translate.google.nr',
                        'translate.google.nu', 'translate.google.pl', 'translate.google.pn',
                        'translate.google.ps', 'translate.google.pt', 'translate.google.ro',
                        'translate.google.rs', 'translate.google.ru', 'translate.google.rw',
                        'translate.google.sc', 'translate.google.se', 'translate.google.sh',
                        'translate.google.si', 'translate.google.sk', 'translate.google.sm',
                        'translate.google.sn', 'translate.google.so', 'translate.google.sr',
                        'translate.google.st', 'translate.google.td', 'translate.google.tg',
                        'translate.google.tk', 'translate.google.tl', 'translate.google.tm',
                        'translate.google.tn', 'translate.google.to', 'translate.google.tt',
                        'translate.google.us', 'translate.google.vg', 'translate.google.vu', 'translate.google.ws')
LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-CN': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'tk': 'turkmen',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URLS_SUFFIX = [re.search('translate.google.(.*)', url.strip()).group(1)
               for url in DEFAULT_SERVICE_URLS]
URL_SUFFIX_DEFAULT = 'cn'


class google_translator():
    def __init__(self, url_suffix="cn", timeout=5, proxies=None):
        if url_suffix not in URLS_SUFFIX:
            self.url_suffix = URL_SUFFIX_DEFAULT
        else:
            self.url_suffix = url_suffix

        self.proxies = proxies
        self.sess = requests.session()
        self.sess.headers = {
            "Referer": "http://translate.google.{}/".format(self.url_suffix),
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "x-goog-batchexecute-bgr":'["",null,null,15,null,null,null,0,"2"]'
        }


        url_base = "https://translate.google.{}".format(self.url_suffix)
        self.url = url_base + "/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&rt=c"
        self.timeout = timeout


    def _package_rpc(self, text, lang_src='auto', lang_tgt='auto'):
        GOOGLE_TTS_RPC = ["MkEWBc"]
        #parameter = [[text.strip(), lang_src, lang_tgt, True], [1]]
        parameter = [[text.strip(), lang_src, lang_tgt, True], [None]]
        escaped_parameter = json.dumps(parameter, separators=(',', ':'))
        rpc = [[[random.choice(GOOGLE_TTS_RPC), escaped_parameter, None, "generic"]]]
        espaced_rpc = json.dumps(rpc, separators=(',', ':'))
        freq_initial = "f.req={}&".format(quote(espaced_rpc))
        freq = freq_initial
        return freq


    def translate(self, text, lang_src='auto', lang_tgt='auto'):
        if self.proxies:
            proxy = {'https':self.proxies}
        else:
            proxy = None

        html = self.sess.get('https://translate.google.cn/').text
        data_str = re.compile(r'window.WIZ_global_data = (.*?);</script>').findall(html)[0]
        data_json = json.loads(data_str)
        print(data_json)
        fsid = data_json['FdrFJe']
        bl = data_json['cfb2h']
        mnsUbf = data_json['mnsUbf']
        return
        self.url = self.url+f'&f.sid={fsid}&bl={bl}'
        text = str(text)
        if len(text) == 0 or len(text) > 5000:
            return

        freq = self._package_rpc(text, lang_src, lang_tgt)

        response = self.sess.post(url=self.url,data=freq,proxies=proxy)
        rtext = response.text.split('\n')
        for line in rtext:
            if "MkEWBc" in line:
                return line
        else:
            return ''


g = google_translator(proxies='127.0.0.1:4780')
print(g.translate(text='每天清晨我去公园散步', lang_src='auto',lang_tgt='en'))
#print(g.translate(text='hello', lang_src='auto',lang_tgt='zh-CN'))

# text = '''ハイレベル自動運転モデルエリア活動弁公室はこのほど「北京市スマートコネクテッドカー政策先行エリア無人化公道テスト管理実施細則」を発表し、正式に「無人化」テストシーンを開放した。段階的に秩序立てて自動運転「無人化」公道テストを展開する。新華網が伝えた。政策によると、開放される「無人化」テスト区間の範囲は、北京市スマートコネクテッドカー政策先行エリアの所在地である北京経済技術開発区内の計100キロメートル以上の都市道路。規定によると、企業は公道テストを実施する際に朝夕のラッシュアワーを回避するうえ、車体に目立つ「無人化」テストマークを貼る必要がある。'''
# for lang_tgt in ['zh-CN','en','ceb','af','sq','am','ar','hy','az','eu','be','bn','bs','bg','ca']:
#     print(g.translate(text=text, lang_src='auto', lang_tgt=lang_tgt))




