# -*- coding: utf-8 -*-
# @Author  : lx
# @IDE ：PyCharm


import re, json, requests
import scrapy
from lxml import etree
import time

'''
该文件是scrapy的spider文件,需要自己修改下；
添加京东店铺主页链接后可采集商品信息和商品评论；
'''

class JingDongSpider(scrapy.Spider):
    name = 'jingdong_spider'
    start_urls = []
    session = requests.session()
    session.keep_alive = False

    def get_json_req(self, url, proxies=None, label=1):
        error = 0
        while True:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
            try:
                data = self.session.get(url=url, headers=headers, proxies=proxies, timeout=10).text
                if label == 2:
                    data = data[20:-2]
                jdata = json.loads(data)
                return jdata
            except Exception as e:
                if error >= 3:
                    break
                error += 1
                continue


    def start_requests(self):
        result = ['https://mall.jd.com/index-1000343441.html?from=pc']
        for shop_url in result:
            yield scrapy.Request(url=shop_url, callback=self.parse)


    def parse(self, response):
        """
        pageInstance_appId ：所有商品列表页的 page-ID
        vender_id : 商品详情所需 ID
        shop_id : 店铺ID
        """
        item_id = {}
        pageInstance_appId = response.xpath('//input[@id="pageInstance_appId"]/@value').get()
        item_id['vender_id'] = response.xpath('//input[@id="vender_id"]/@value').get()
        shop_id = response.xpath('//input[@id="shop_id"]/@value').get()
        all_href = 'https://mall.jd.com/view_search-{}-0-99-1-24-1.html'.format(pageInstance_appId)
        yield scrapy.Request(url=all_href, callback=self.parse_list, meta={'item_id': item_id})


    def parse_list(self, response):
        """
        appId pageInstance_id instanceid 提取列表页接口参数
        """
        item_id = response.meta['item_id']
        appId = response.xpath('//input[@id="pageInstance_appId"]/@value').get()
        pageInstance_id = response.xpath('//input[@id="pageInstance_id"]/@value').get()
        instanceid = response.xpath('//div[@class="m_render_structure loading"]/@m_render_layout_instance_id').get()
        if not appId or not pageInstance_id or not instanceid:
            raise Exception("LIST ID NOT FOUND")
        goods_url = f'https://module-jshop.jd.com/module/allGoods/goods.html?callback=jQuery9812889&appId={appId}&pageInstanceId={pageInstance_id}&searchWord=&pageNo=1&direction=1&instanceId={instanceid}&modulePrototypeId=55555&moduleTemplateId=905542'
        print(goods_url)
        yield scrapy.Request(url=goods_url, callback=self.parse_list_info, meta={'item_id': item_id})


    def parse_list_info(self, response):
        """ 1、列表页商品URL提取
            2、提取下一页URL
        :param response:
        :return:
        """
        item_id = response.meta['item_id']
        doc = response.text
        '''通过关键词控制翻页'''
        if 'pageGoodsList(1 + 1, this)' in doc:
            strurl = str(response.url)
            page = re.findall('pageNo=(\d+)&', strurl)[0]
            next_page = strurl.replace(f'&pageNo={page}&', f'&pageNo={int(page) + 1}&')
            yield scrapy.Request(url=next_page, callback=self.parse_list_info, meta={'item_id': item_id})

        HTML_CONTENT = json.loads(doc[14:-1])['HTML_CONTENT_KEY']
        e = etree.HTML(HTML_CONTENT)
        # goods_count = e.xpath('//span[@id="J_resCount"]/text()')[0]
        for li in e.xpath('//div[@id="J_GoodsList"]/ul/li'):
            goods_url = 'https:' + li.xpath('./div/div[@class="jGoodsInfo"]/div[@class="jDesc"]/a/@href')[0]

            yield scrapy.Request(url=goods_url, callback=self.parse_detail, meta={'item_id': item_id})
            yield scrapy.Request(url=goods_url, callback=self.parse_jd)


    def parse_detail(self, response):
        """
        解析详情页面
        """
        item = {}
        platform_good_id = re.findall('item.jd.com/(.*?)\.html', str(response.url))[0]
        item_id = response.meta['item_id']
        vender_id = item_id['vender_id']

        goods_name = ''.join(''.join(response.xpath('//div[@class="sku-name"]/text()').getall()).split())

        goods_pic = ['https:' + i for i in response.xpath('//div[@id="spec-list"]/ul/li/img/@src').getall()]
        goods_brand = response.xpath('//ul[@id="parameter-brand"]/li/@title').get()
        if not goods_brand:
            goods_brand = response.xpath('//div[@class="crumb fl clearfix"]/div[last()-2]//a/text()').get()
        goods_sku = response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/text()').getall()

        category = False
        for li in goods_sku:
            if '类别' in li or '种类' in li or '分类' in li:
                category = li.split('：')[1]
                break
        if not category:
            category = response.xpath('//div[@class="crumb fl clearfix"]/div[5]/a/text()').get()

        goods_type = response.xpath('//div[@id="choose-attr-1"]/div[@class="dd"]/div/@data-value').getall()  # 选择种类
        skuIdList = response.xpath('//div[@id="choose-attr-1"]/div[@class="dd"]/div/@data-sku').getall()
        # skuId = response.xpath('//div[@id="choose-attr-1"]/div[@class="dd"]/div/@data-sku').get()

        item['platform_good_id'] = 'jd' + str(platform_good_id)
        item['goods_name'] = goods_name
        item['brand'] = goods_brand  # 品牌
        item['category'] = category  # 品类
        item['creator'] = None

        # 不同 skuid 对应商品价格不同
        item['unit_price'] = None
        price = 0
        if not skuIdList:
            skuIdList.append(platform_good_id)


        # todo 获取不同sku的平均价格
        for skuId in skuIdList:
            price_url = f'https://item-soa.jd.com/getWareBusiness?skuId={skuId}&cat=12218%2C13586%2C12250&area=7_438_444_36068&shopId={platform_good_id}&venderId={vender_id}&paramJson=%7B%22platform2%22%3A%221%22%2C%22colType%22%3A0%2C%22specialAttrStr%22%3A%22p0ppp1ppppppppppppppp%22%2C%22skuMarkStr%22%3A%2200%22%7D&num=1'
            pdata = self.get_json_req(price_url)
            goods_price = float(pdata['price']['p'])
            price += goods_price
            time.sleep(1)
        if price != 0:
            item['unit_price'] = price / len(skuIdList)

        # print(item['unit_price'],platform_good_id)
        yield item

        '''
        '取第一个SKU-ID'
        # score = 0 默认 , score = 1 差评 , score = 2 中评 , score = 3 好评 , score = 5 追评
        comment_url = f'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={skuId}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        cdata = self.get_json_req(comment_url,label=2)

        imageListCount = cdata['imageListCount']                                # 晒图
        videoCount = cdata['productCommentSummary']['videoCount']               # 晒视频
        defaultGoodCount = cdata['productCommentSummary']['defaultGoodCount']   # 默认好评
        afterCount = cdata['productCommentSummary']['afterCount']               # 追评
        commentCount = cdata['productCommentSummary']['commentCount']
        goodCount = cdata['productCommentSummary']['goodCount']                 # 好评
        goodRate = cdata['productCommentSummary']['goodRate']                   # 好评%
        generalCount = cdata['productCommentSummary']['generalCount']           # 中评
        generalRate = cdata['productCommentSummary']['generalRate']             # 中评%
        poorCount = cdata['productCommentSummary']['poorCount']                 # 差评
        poorRate = cdata['productCommentSummary']['poorRate']                   # 差评%
        score1Count = cdata['productCommentSummary']['score1Count']
        score2Count = cdata['productCommentSummary']['score2Count']
        score3Count = cdata['productCommentSummary']['score3Count']
        score4Count = cdata['productCommentSummary']['score4Count']
        score5Count = cdata['productCommentSummary']['score5Count']

        for hotComment in cdata['hotCommentTagStatistics']:
            hotword = hotComment['name']

        comment_list = []
        for comment in cdata['comments']:
            id = comment['id']
            guid = comment['guid']
            content = comment['content']
            creationTime = comment['creationTime']
            userImageUrl = comment['userImageUrl']
            score = comment['score']
            replyCount = comment['replyCount']      # 回复
            usefulVoteCount = comment['usefulVoteCount']  # 点赞
            productColor = comment['productColor']  # 规格
            productSize = comment['productSize']    # 规格

            replies = comment['replies']  # 回复
            replies_comment = replies[0]['content']
            replies_nickname = replies[0]['nickname']
            replies_userImage = replies[0]['userImage']
            replies_creationTime = replies[0]['creationTime']
            replies_id = replies[0]['id']

            comment_list.append(content)
        '''


    def parse_jd(self, response):
        goods_sql_id = response.meta['goods_sql_id']
        skuId = response.xpath('//div[@id="choose-attr-1"]/div[@class="dd"]/div/@data-sku').get() #取第一个SKU-ID
        if not skuId:
            skuId = response.xpath('//a[@class="notice J-notify-sale"]/@data-sku').get()
        # score = 0 默认 , score = 1 差评 , score = 2 中评 , score = 3 好评 , score = 5 追评
        if not skuId:
            print("GOODS-ID: %s NOT SKUID"%goods_sql_id)
            raise IndexError("GOODS-ID: %s NOT SKUID"%goods_sql_id)
        for page in range(0,1):
            comment_url = f'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={skuId}&score=0&sortType=5&page={page}&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=comment_url,callback=self.parse_jdcomment,
                                 meta={'goods_sql_id':goods_sql_id},dont_filter=True)


    def parse_jdcomment(self,response):
        goods_sql_id = response.meta['goods_sql_id']
        if not response.text:
            yield scrapy.Request(url=response.url,callback=self.parse_jdcomment,
                                 meta={'goods_sql_id':goods_sql_id},dont_filter=True)
        cdata = json.loads(response.text[20:-2])

        #for hotComment in cdata['hotCommentTagStatistics']:
        #    hotword = hotComment['name']
        commentCount = cdata['productCommentSummary']['commentCount']
        if commentCount==0 or commentCount==1:
            print(goods_sql_id,"无评论内容")
            return

        for comment in cdata['comments']:
            item = {}
            item['comment_id'] = 'jd'+str(comment['id'])
            item['goods_id'] = goods_sql_id
            item['comment_content']  = comment['content']
            item['creator'] = None
            score = comment['score']
            if score>=4:
                comment_type = '好评'
            elif score==3:
                comment_type = '中评'
            else:
                comment_type = '差评'
            item['comment_type'] = comment_type
            yield item

