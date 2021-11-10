import requests,re,json

sess = requests.session()
headers={
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.bing.com',
    'referer': 'https://www.bing.com/translator/',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"93.0.4577.82"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model':'',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'cookie': '',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
}

doc = sess.get("https://www.bing.com/translator",headers=headers).text

IG = re.findall('IG:"(.*?)"',doc,re.S)[0]
IID = re.findall('data-iid="(.*?)"',doc,re.S)[0]
_key, _token = re.findall('var params_RichTranslateHelper = \[(\d+),"(.*?)",',doc,re.S)[0]

url = f'https://www.bing.com/ttranslatev3?isVertical=1&&IG={IG}&IID={IID}'


text = '''829年英国政府颁布天主教徒解放法，取消对爱尔兰天主教徒的歧视性政策。随着爱尔兰自治运动的开展，爱尔兰的新教徒担心爱尔兰的自治或独立将使他们成为一个天主教占多数的国家中的少数群体，因而成立联合派，主张爱尔兰继续留在联合王国之内。
20世纪初，随着爱尔兰自治运动的日益强大，阿尔斯特省的新教徒组织阿尔斯特志愿军；作为回应，天主教徒组织爱尔兰志愿军。
1918年的大选中，在爱尔兰，主张爱尔兰独立的新芬党赢得73%的选票，然而在阿尔斯特9郡中新教徒占优势的6郡，新芬党都输掉选举。
1920年，英国政府颁布爱尔兰仲裁法，将阿尔斯特省新教徒占优的6郡组成北爱尔兰，阿尔斯特省剩下的3郡与其他3省合并成南爱尔兰。
1921年，爱尔兰独立战争结束以后，根据英爱条约，爱尔兰自由邦成立，北部阿尔斯特省中的6郡成为北爱尔兰，并在条约签署后一个月内自主决定是否留在爱尔兰自由邦内，而北爱尔兰议会选择退出爱尔兰自由邦，留在联合王国之内。大多数北爱尔兰人（联合派）希望留在英国，但一个举足轻重的少数派（民族派）希望加入爱尔兰共和国。
原因：在英国统治爱尔兰岛的时期，英国在爱尔兰岛北方有大量的新教徒移民，新教徒后来占人口的多数。爱尔兰人信天主教，属于凯尔特人。爱尔兰独立，但以新教为主的北部6郡拒绝独立，选择继续留在英国，以地区的地位加入英。
1960年代到1990年代两派之间的斗争武装化。
1972年北爱尔兰的自治权为此被取消。
1990年代中开始，两派的主要半军事组织达成一个不十分可靠的停火协议。
1998年工党政府在北爱尔兰和平协议签署后同意北爱组建地方自治政府。
2002年10月14日，英国政府宣布中止北爱地方自治政府的运作，把北爱尔兰地区的控制权重新收归中央政府。
2007年5月8日，民主统一党和新芬党达成协议后，四党组成的联合政府宣誓就职，这意味着北爱正式恢复分权自治政府。
2010年2月，民主统一党和新芬党就移交警务和司法权问题达成协议，北爱的警务和司法权从英议会移交至北爱地方议会。
2015年9月，联合政府因爱尔兰共和军前成员遇刺事件引发危机，北爱地方政府首席部长彼得·罗宾逊（Peter Robinson）率多位部长辞职。12月，阿莱娜·福斯特（Arlene Foster）当选民主统一党新领袖并担任北爱地方政府首席部长，新芬党副领袖马丁· 麦吉尼斯（Martin McGuinness）任副首席部长。
2017年1月，麦吉尼斯宣布辞职，以抗议福斯特力推的“可再生热能激励项目”。根据1998年和平协议相关安排，副首席部长辞职后，首席部长不能单独完全履职，北爱尔兰政府无法正常运转。3月，北爱尔兰提前举行议会选举。北爱尔兰两大政党民主统一党和新芬党得票领先。在选举产生的90名议员中，民主统一党占28人，新芬党27人，均未过半。
2020年1月，民主统一党和新芬党达成联合组阁协议，阿莱娜·福斯特续任首席部长，新芬党副领袖米歇尔·奥尼尔（Michelle O’Neil）出任副首席部长，北爱地方政府恢复运作。'''
to = 'zh-Hans'
data={
    'fromLang': 'auto-detect',
    'text': text,
    'to': to,
    'token': _token,
    'key': _key,
}
datas = sess.post(url,headers=headers,data=data).text
print(datas)
