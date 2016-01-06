#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import time
import json
from backend.redisHelper import RedisHelper
channel = 'FM90.0'
redisSrv = RedisHelper()
result = redisSrv.subscribe(channel)
templates = {
    'template1': {
        'cpu':{
            'interval':10,
            'pluginName':'getCpuInfo',
            'lastTime':0
            },
        'mem':{
            'interval':10,
            'pluginName':'getMemInfo',
            'lastTime':0
            },
        'load':{
            'interval':10,
            'pluginName':'getLoadInfo',
            'lastTime':0    
            }   
              
        },
    'template2': {
        'cpu':{
            'interval':15,
            'pluginName':'getCpuInfo',
            'lastTime':0
            },
        'mem':{
            'interval':10,
            'pluginName':'getMemInfo',
            'lastTime':0
            },
        'load':{
            'interval':20,
            'pluginName':'getLoadInfo',
            'lastTime':0    
            }   
              
        },
}
for k,v in templates.items():
    redisSrv.set(k, json.dumps(v))

hosts = {
    'linux2333':'template1',
    'linux3333':'template2',
    'linux4333':'template1',
}
for k,v in hosts.items():
    redisSrv.set(k, v)


while True:
    data = result.parse_response()
    print data[2]