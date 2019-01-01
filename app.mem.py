#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging;logging.basicConfig(level=logging.INFO)
from aiohttp import web
from multidict import CIMultiDict

import uuid,os,memcache,random

import platform
if(platform.system()=='Linux'):
    USEIP = '192.168.31.130'
else:
    USEIP = '127.0.0.1'

APP_PATH = os.path.split(os.path.realpath(__file__))[0]
PHOTO_PATH=os.path.join(APP_PATH, 'photos')
STATIC_PATH=os.path.join(APP_PATH,'static')

# /usr/local/memcached/bin/memcached -p 12001 -m 128 -P /tmp/memcache.pid -d
mc=memcache.Client([
    '192.168.31.130:12001',
    # '192.168.31.132:2001',
    # '192.168.31.133:2001'
])

def index(request):
    return web.Response(body=b'<a href="p">who are you :)</a>', status=200,
                 reason=None, text=None, headers=None, content_type='text/html',
                 charset=None)

async def upload(request):
    header = CIMultiDict()
    header.add('Access-Control-Allow-Origin', '*')

    postdata= await request.post()
    if 'file' not in postdata.keys(): return web.json_response(data={'code':-1,'msg':'file not found','data':''},headers=header)
    file = postdata['file']

    puuid= uuid.uuid1().hex# + os.path.splitext(file.name)[1]
    fpname=os.path.join(PHOTO_PATH, puuid)
    with open(fpname,'wb') as op:
        op.write(file.file.read())


    return web.json_response(data={'code':0,'msg':'ok','data':puuid},headers=header)

    # header.add('Access-Control-Allow-Methods', '*')
    # header.add('Access-Control-Allow-Headers', 'x-requested-with,content-type')

def p(request):
    uuid = request.GET.get('uuid')
    #fname = request.match_info.get('fname')
    if uuid == None:
        ps=os.listdir(PHOTO_PATH)
        uuid = random.choice(ps)
        uuid = os.path.splitext(uuid)[0]

    header = CIMultiDict()
    header.add('X-mem-key', uuid)
    mgs = mc.get(uuid)
    if mgs:
        logging.info('读取缓存:' + uuid)
        header.add('X-mem-cache', 'HIT')
        return web.Response(body=mgs, content_type='image/jpeg', headers=header)
    else:
        fp = os.path.join(PHOTO_PATH, uuid)
        if not os.path.exists(fp):
            logging.info('文件不存在:' + uuid)
            header.add('X-mem-cache', 'NONE')
            return web.Response(body=b'', content_type='image/jpeg', headers=header)
        with open(os.path.join(PHOTO_PATH, uuid), 'rb') as fo:
            rs = fo.read()
            mrs = mc.set(uuid, rs, 1 * 60)
            logging.info('写入缓存:' + uuid)
            header.add('X-mem-cache', 'MISS')
            return web.Response(body=rs, content_type='image/jpeg', headers=header)



def getPhotoCache(uuid):
    # name = os.path.splitext(uuid)[0]
    mgs = mc.get(uuid)
    if mgs:
        logging.info('读取缓存:' + uuid)
        return mgs
    else:
        fp = os.path.join(PHOTO_PATH, uuid)
        if not os.path.exists(fp):
            logging.info('文件不存在:' + uuid)
            return b''
        with open(os.path.join(PHOTO_PATH, uuid), 'rb') as fo:
            rs = fo.read()
            mrs = mc.set(uuid, rs, 1 * 60)
            logging.info('写入缓存:' + uuid)
            return rs

def test(request):
    header = CIMultiDict()
    header.add('Access-Control-Allow-Origin', '*')
    return web.json_response(data={'code':0,'msg':'ok','data':'all ok'},headers=header)

async def init(loop):
    if not os.path.exists(PHOTO_PATH):
        os.mkdir(PHOTO_PATH)
    app=web.Application(loop=loop,debug=True)
    app.router.add_route('*','/',index)
    app.router.add_route('*','/u',upload)
    app.router.add_route('*','/p',p)
    app.router.add_route('*','/imageserver/p',p)
    app.router.add_route('*','/test/',test)
    srv=await loop.create_server(app.make_handler(),USEIP,7003)
    logging.info('system start at port http://'+USEIP+':7003')
    return srv


if  __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()