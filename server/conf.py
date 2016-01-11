#!/usr/bin/env python
#_*_coding:utf-8_*_
from backend.redisHelper import *
import json
from ecdsa.ecdsa import __main__

redisSrv = RedisHelper()
class BaseMonitor:
    def __init__(self, name, interval, pluginName, threshold):
        self.name = name
        self.interval = interval
        self.pluginName = pluginName
        self.threshold = threshold

class DefaultLoadMonitor(BaseMonitor):
    def __init__(self):
        name = 'load'
        interval = 7
        pluginName = 'getLoadInfo'
        lasttime = 0
        threshold = {
            'load1':[4, 9],
            'load5':[3, 7],
            'load15':[3, 9],
            }
        BaseMonitor.__init__(self, name, interval, pluginName, lasttime, threshold)
class DefaultMemMonitor(BaseMonitor):
    def __init__(self):
        name = 'load'
        interval = 7
        pluginName = 'getMemInfo'
        threshold = {
            'MemAvailable':['percentage', 20,10],
            'Cached':['percentage', 20,10],
            'Buffers':['percentage', 20,10],
            }
        BaseMonitor.__init__(self, name, interval, pluginName, threshold)

class DefaultCpuMonitor(BaseMonitor):
    def __init__(self):
        name = 'cpu'
        interval = 7
        pluginName = 'getCpuInfo'
        threshold = {
            'iowait':['percentage', 5.5, 90],
            'system':['percentage', 5, 90],
            'idle':['percentage', 20, 10],
            'user':['percentage', 80, 90],
            'steal':['percentage', 80, 90],
            'nice':[None, 80, 90],
            }
        BaseMonitor.__init__(self, name, interval, pluginName, threshold)

class BaseTemplate:
    def __init__(self, cpu, load, mem):
        self.Items = {
            'cpu': cpu,
            'load': load,
            'mem': mem
            }
    
    @property
    def service(self):
        return self.__services
    
    @property
    def editCpu(self):
        return self.__services['cpu'] 
    
def init_template():
    t1 = BaseTemplate(cpu=DefaultCpuMonitor(), mem=DefaultMemMonitor(),load=DefaultLoadMonitor())
    t1.editCpu().interval = 10
    return {'template1': t1}   

def push_config_to_redis(redisSrv, templates):
    for key, template in templates.items():
        config = {}
        for k, v in template.service.items():
            config[k] = {'interval': v.interval, 'pluginName': v.pluginName, 'lasttime': 0}
            for tk, tval in v.threshold.items():
                config[k][tk] = tval
            redisSrv.set(key, json.dumps(config))

def init_hostname_certname():
    hosts = {
        'linux2333.puppet.com': 'template1',
        'windows2333.puppet.com': 'template1',
             
        }
    #主机名对应的模板添加到redis
    for k,v in hosts.items():
        redisSrv.set(k, v)
def run(result):
    while True:
        data = result.parse_response()
        getInfo = json.loads(data[2])
        if getInfo['level'] == 3:
            print '\033[31m%s\033[0m'%getInfo
        if getInfo['level'] == 2:
            print '\033[33m%s\033[0m'%getInfo
        if getInfo['level'] == 1:
            print '\033[32m %s \033[0m'%getInfo
        print '================================================='
        
if __name__ == '__main__':
    redisSrv = RedisHelper()
    result = redisSrv.subscribe('FM90.0')
    templates = init_template()
    init_hostname_certname()
    push_config_to_redis(redisSrv, templates)
    run(result)