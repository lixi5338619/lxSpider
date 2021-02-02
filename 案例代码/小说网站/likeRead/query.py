#查找文件列表，判断是否保存过该小说，若保存过则从记录开始

import json
import os

def query(book_name,title,urlList,rename):
    if rename:
        if os.path.exists("%s(旧).js"%book_name):
            os.remove("%s(旧).js"%book_name)
            os.remove("%s(旧).txt"%book_name)
        os.rename("%s.js"%book_name,"%s(旧).js"%book_name)
        os.rename("%s.txt"%book_name,"%s(旧).txt"%book_name)
    if os.path.isfile("%s.js"%book_name):
        with open('%s.js'%book_name,'r',encoding='utf-8')as fp:
            store = json.load(fp)
        index = 0
        for i in store:
            for y in range(len(title)):
                if i['title'] == title[y]:
                    index = y+1
        del title[:index]
        del urlList[:index]
        query_all = {
            "title":title,
            "urlList":urlList,
            "store":store
        }
        return query_all
    return False