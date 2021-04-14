from spider import *
import tornado.ioloop
import tornado.web
import platform

if platform.system() == "Windows":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Zlibraty(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_query_argument('keyword', '')
        searchtype = self.get_query_argument('searchtype', 'Content')
        item = get_zlibraty(keyword=keyword,searchtype=searchtype)
        self.write(item)

class Weipu(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_query_argument('keyword', '')
        searchtype = self.get_query_argument('searchtype', 'Content')
        item = get_weipu(keyword=keyword,searchtype=searchtype)
        self.write(item)

class Jstor(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_query_argument('keyword', '')
        searchtype = self.get_query_argument('searchtype', 'Content')
        item = get_jstor(keyword=keyword,searchtype=searchtype)
        self.write(item)

class Wanfang(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_query_argument('keyword', '')
        searchtype = self.get_query_argument('searchtype', 'Content')
        item = get_wanfang(keyword=keyword,searchtype=searchtype)
        self.write(item)

class Zhiwang(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_query_argument('keyword', '')
        searchtype = self.get_query_argument('searchtype', 'Content')
        item = get_zhiwang(keyword=keyword,searchtype=searchtype)
        self.write(item)

class Oalib(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_query_argument('keyword', '')
        searchtype = self.get_query_argument('searchtype', 'Content')
        item = get_oalib(keyword=keyword,searchtype=searchtype)
        self.write(item)

def make_app():
    return tornado.web.Application([
        (r"/get_weipu", Weipu),
        (r"/get_jstor", Jstor),
        (r"/get_zhiwang", Zhiwang),
        #(r"/get_wanfang", Wanfang), # 万方更新了
        (r"/get_zlibraty", Zlibraty),
        (r"/get_oalib", Oalib),
    ])

if __name__ == "__main__":
    app = make_app()                            # 创建一个应用对象
    app.listen(port=8888,address='0.0.0.0')     # 设置端口,访问ip
    tornado.ioloop.IOLoop.current().start()     # 启动 web程序，开始监听端口的连接
