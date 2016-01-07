#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import time
import json
from backend.redisHelper import RedisHelper
from plugins import plugin_api

channel = 'FM90.0'
redis_cli = RedisHelper()
hostname='linux2333'
tempName = redis_cli.get(hostname)
config = json.loads(redis_cli.get(tempName))

while True:
    for k,v in config.items():
        interval, lasttime = v['interval'], v['lastTime']
        currenttime = time.time()
        if (currenttime - lasttime) < interval:
            pass
        else:
            pluginName = v['pluginName']
            func = getattr(plugin_api, pluginName)   #反射参数一为模块，参数二为方法
            data = func()
            if k == 'load':
                
                getData = data['load5']
                warm, error = v['load5']
                getData = float(getData)
                if getData > error:
                    data['level'] = 3
                elif getData > warm:
                    data['level'] = 2
                else:
                    data['level'] = 1
            else:
                data['level'] = 1
            redis_cli.fabu(json.dumps(data)
            config[k]['lasttime'] = currenttime
