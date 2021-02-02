#将解析获得的章节名及章节内容保存

import json

def save(book_name,store):
    with open("%s.js"%book_name,"w",encoding='utf-8') as fp:
        json.dump(store,fp,ensure_ascii=False)
    with open("%s.txt"%book_name,"w",encoding='utf-8')as fp:
        for i in store:
            fp.write(i["title"])
            fp.write(i["store"]+'\n')
