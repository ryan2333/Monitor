#!/usr/bin/env python
#coding:utf-8
import time
import json
from backend.redisHelper import RedisHelper
from plugins import plugin_api

redis_cli = RedisHelper()
certname = 'linux2233.puppet.com'


#根据主机名获取模板名称 'linux2233.com -- > template_1'
template_name = redis_cli.get(certname)
print template_name
config = json.loads(redis_cli.get(template_name))

while True:
    for key,value in config.items():
        currenttime,interval,lasttime = time.time(),value['interval'],value['last_time']
        if (currenttime-lasttime) < interval:
            pass
        else:
            plugin_name = value['plugin_name']
            func = getattr(plugin_api, plugin_name)
            data = func()
            if key == 'load':
                get = data['load5']
                warm,error = value['load5']
                get = float(get)
                print get,warm,error
                if get>error:
                    data['level'] = 3
                elif get>warm:
                    
                    data['level'] = 2
                else:
                    data['level'] = 1
            else:
                data['level'] = 2
            redis_cli.public(json.dumps(data))
            config[key]['last_time'] = currenttime
    time.sleep(1)