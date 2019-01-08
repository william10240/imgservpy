#Python 图片服务


docker启动: docker-compsoe up -d,启动后端口为 83

原生启动: Python3 app.js,启动后端口为 80

启动后:
http://localhost:83/p  随机显示一张图片

http://localhost:83/p?uuid=5fdc39c27d5d11e6ba7cb827eb6f00ae 显示指定一张图片

[post]http://localhost:83/u (file) 上传一张图片,返回数据的data为存储的uuid,返回code不为0则表示出错

```
{
    "code": 0,
    "msg": "ok",
    "data": "b95a32ec0d7f11e990a4a8667f057892"
}
```
![upload image](https://raw.githubusercontent.com/williamyan1024/img/master/py_ImageServer1.jpg)

todo:

通过配置文件配置连接地址和链接方式

添加鉴权防盗链

添加在线压缩和压缩后缓存功能

添加远程图片读取(热更新)功能
