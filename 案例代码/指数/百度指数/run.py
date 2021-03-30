import json
from utils import test_cookies
from baidu_index import BaiduIndex

cookies = "BDUSS=lNvbFZLS0JERmpZQTd0QktJSFh3a2RYRXZoUEtwN3JWTXVMQkdHc3dtWlpnU3hnRVFBQUFBJCQAAAAAAAAAAAEAAADl2HYhxNq439Chz6YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFn0BGBZ9ARgQ"


if __name__ == "__main__":
    print(test_cookies(cookies))

    keywords = ['在线英语']


    baidu_index = BaiduIndex(
        keywords=keywords,
        start_date='2019-12-29',
        end_date='2021-01-17',
        cookies=cookies,
        area=0, # 地区    0:全国     911:北京
    )

    index_list = []
    import csv
    f = open('在线英语百度指数/'+keywords[0]+'.csv', 'w', encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["date","index"])


    for index in baidu_index.get_index():
        print(index)
        index_list.append(index)

    e,ee,dd = 0,[],[]
    for i in range(1, len(index_list)):
        if i % 7 == 0:
            ee.append(round(e/7))
            dd.append(index_list[i]['date'])
            e = 0
        else:
            e += float(index_list[i]['index'])

    for d,e in zip(dd,ee):
        csv_writer.writerow([d,e])


    #index_dict = {'index': index_list}
    #with open('test.json', 'a', encoding="utf-8") as f:
    #    json.dump(index_dict, f, ensure_ascii=False, indent=4)
    #    f.write('\n')
