# python 实时语音转写

本demo测试时运行的环境为：Windows + Python3.7

本demo测试成功运行时所安装的第三方库及其版本如下，您可自行逐一或者复制到一个新的txt文件利用pip一次性安装：
- cffi==1.12.3
- gevent==1.4.0
- greenlet==0.4.15
- pycparser==2.19
- six==1.12.0
- websocket==0.2.1
- websocket-client==0.56.0

语音听写流式 WebAPI 接口调用示例 接口文档（必看）：https://doc.xfyun.cn/rest_api/语音听写（流式版）.html

webapi 听写服务参考帖子（必看）：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38947&extra=

语音听写流式WebAPI 服务，热词使用方式：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--个性化热词，
设置热词

注意：热词只能在识别的时候会增加热词的识别权重，需要注意的是增加相应词条的识别率，但并不是绝对的，具体效果以您测试为准。

语音听写流式WebAPI 服务，方言试用方法：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--识别语种列表
可添加语种或方言，添加后会显示该方言的参数值

错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
