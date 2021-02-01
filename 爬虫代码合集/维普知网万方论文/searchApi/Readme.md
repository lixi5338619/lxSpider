## 使用文档：
**需求简介**
从 《维普数据网、中国知网、万方数据网、Jstor、Zlibraty、Oalib》获取检索结果，通过请求接口返回数据


**运行环境：** 
|环境依赖| 安装方法|
|--|--|--|
| python3 |  百度|
| requests|  pip install requests|
| tornado  | pip install tornado   |





**接口说明**

|接口名称|  请求方式| 接口简介|
|--|--|--|
| get_weipu | Get  | 维普网    |
| get_zhiwang| Get   |    中国知网      |
| get_wanfang| Get   |万方网|
| get_jstor|Get    |   Jstor网   |
| get_zlibraty|Get    |  Zlibraty网    |
| get_oalib|Get    |  Oalib  |


**请求接口参数**
|参数名|  格式类型| 简介|
|--|--|--|
|keyword |字符串|要搜索的内容|
|searchtype |字符串| 搜素类型|
- searchtype 示例：  
	- searchtype = Content : 全文搜索  
	- searchtype = Theme : 主题搜索   
	- searchtype = Author : 作者搜索   
	- searchtype = KeyWd : 关键词搜索

（searchtype支持 : Jstor、Oalib、万方、知网, 其他选择默认检索方式）


**请求端口**： 8888

**访问示例**：  **(注意参数的大小写**)
```python
http://127.0.0.1:8888/get_zlibraty?keyword=医学论文&searchtype=Content
http://127.0.0.1:8888/get_weipu?keyword=古文化
http://127.0.0.1:8888/get_zhiwang?keyword=python&searchtype=Author
```

---

**返回数据示例**：
请求接口： http://127.0.0.1:8888/get_zhiwang?keyword=python&searchtype=Author
返回格式： Json

|参数名|  格式类型| 简介|备注|
|--|--|--|--|
|articleList|List|搜素详情|     返回文章列表      |
|success|String| 是否搜索到|   返回True，Flase   |
|recordcount| Int| 查询结果| 查询到多少记录|
 |title| String| 标题| |
 |sources| String| 出处来源| |
 |author| String| 作者|部分没有作者 |
 |desc| String| 简介| 部分没有简介|
```json
{
    "articleList":[
        {
            "title":"为什么要写《对比Excel，轻松学习Python数据分析》",
            "sources":"张俊红 新华书目报 2019-03-28报纸",
            "author":"张俊红",
            "desc":"《对比Excel,轻松学习Python数据分析》既是一本数据分析的书,也是一本Excel数据分析的书,同时还是一本Python数据分析的书。在互联网上,无论是搜索数据分析,还是搜索Excel数据分析,亦或是搜索Python数据分析,我们都可..."
        },
        {
            "title":"新形势下反毒技术面临的挑战",
            "sources":"Python 计算机世界 2002-10-14报纸",
            "author":"Python",
            "desc":"人们经常会问：“安装了杀毒软件，为什么还会中毒？而且损失越来越大？”这个现实问题给炒作得热火朝天的“病毒经济”当头一棒！探讨预防病毒的方法应该从病毒发展趋势、技术面临的挑战来冷静分析。 $$一、病毒未来..."
        }
    ],
    "success":true,
    "recordCount":"2"
}
```

---
## 如果运行报错：
如果你是 Python3.8 的 tornado报错NotImplementedError：
就把servers.py文件中，下面代码的注释解开
```python
import platform 
if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

---
