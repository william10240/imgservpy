#Python 图片服务

app.mem.py  使用memcache做缓存
app.redis.py    使用redis做缓存

启动服务: Python3 app.redis.js

http://localhost/p  随机显示一张图片

http://localhost/p?uuid=xxxxxxx  显示指定一张图片

[post]http://localhost/u (file) 上传一张图片,返回数据的data为存储的uuid

```
{
    "code": 0,
    "msg": "ok",
    "data": "b95a32ec0d7f11e990a4a8667f057892"
}
```

todo:

memcache和redis调用合并

通过配置文件配置连接地址和链接方式

添加鉴权防盗链

添加在线压缩和压缩后缓存功能

添加远程图片读取(热跟新)功能





tip:任重而道远