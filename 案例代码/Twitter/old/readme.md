
##推特采集案例：

## 流程:

- 先从 api/graphql 获取 rest_id

- 然后通过 rest_id 采集动态列表

- 将推文数据保存到csv中

###备注：

username 是链接中的名字 'https://twitter.com/POTUS'

main方法中需要填写 csrf_token和authorization和cookies

这三个参数都在headers中

---

用户信息数据没有存储，自行修改