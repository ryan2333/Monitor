#!/usr/bin/env python
#coding:utf-8


from backend.redisHelper import RedisHelper
import  json

class BaseService:  
    def __init__(self,name,interval,pluginname,triggers):
        self.name = name
        self.interval = interval
        self.last_time = 0
        self.plugin_name = pluginname
        self.triggers = triggers
    
class DefaultCpuService(BaseService):
    def __init__(self):
        name = 'cpu'
        interval = 5
        plugin_name = 'getCpuInfo'
        triggers = {}
        BaseService.__init__(self, name, interval, plugin_name, triggers)

class DefaultMemoryService(BaseService):
    def __init__(self):
        name = 'memory'
        interval = 3
        plugin_name = 'getMemInfo'
        triggers = {}
        BaseService.__init__(self, name, interval, plugin_name, triggers)

class DefaultLoadService(BaseService):
    def __init__(self):
        name = 'load'
        interval = 6
        plugin_name = 'getLoadInfo'
        triggers = {
                'load1': [0.01,0.02],
                'load5': [0.02,0.05],
                'load15': [0.05,0.1],
        }
        BaseService.__init__(self, name, interval, plugin_name, triggers)
        
class BaseTemplate:
    
    def __init__(self,cpu,memory,load):
        self.__services = {
                'cpu': cpu,
                'memory': memory,
                'load':  load,
            }
    @property
    def service(self):
        return self.__services

    @property
    def editcpu(self):
        return self.__services['cpu']


'''
templates = {
    'template_1':{
        'cpu':{'interval':7,
                'plugin_name':'get_cpu_info',
                'last_time':0
            },
        'load':{'interval':5,
                'plugin_name':'get_load_info',
                'last_time':0,
                'load5':[0.02,0.1],
            },
        'memory':{'interval':2,
                'plugin_name':'get_memory_info',
                'last_time':0
            }
    },
    'template_2':{
        'cpu':{'interval':4,
                'plugin_name':'get_cpu_info',
                'last_time':0
            },
        'load':{'interval':6,
                'plugin_name':'get_load_info',
                'last_time':0
            },
        'memory':{'interval':20,
                'plugin_name':'get_memory_info',
                'last_time':0
            }
    }
 }
 '''
   
#所有的模板添加到redis
def init_template():
    t1 = BaseTemplate(cpu=DefaultCpuService(),memory=DefaultMemoryService(),load=DefaultLoadService())
    t1.editcpu.interval = 3
    return {'template_1':t1}

def push_config_to_redis(rediscli,templates):
    for key,template in templates.items():
        config = {}
        for k,v in template.service.items():
            config[k] = {'interval':v.interval,'plugin_name':v.plugin_name,'last_time':0} 
            for tk,tval in v.triggers.items():
                config[k][tk] = tval
        rediscli.set(key,json.dumps(config))

def init_hostname_certname(): 
    hosts = {
        'linux2233.puppet.com':'template_1',
        'windows2233.puppet.com':'template_1',
        'linux22101.zjz.com':'template_1',
    }
    #主机名对应的模板添加到redis
    for key,value in hosts.items():
        rediscli.set(key, value)

def run(result):    
    
    while True:
        data = result.parse_response()
        get_info = json.loads(data[2])
        if get_info['level'] == 3:
            print '\033[31m %s \033[0m' %(get_info,)
        elif get_info['level'] == 2:
            print '\033[33m %s \033[0m' %(get_info,)
        elif get_info['level'] == 1:
            print '\033[32m %s \033[0m' %(get_info,)
        print '============================'
        
if __name__ == '__main__':
    rediscli = RedisHelper()
    result = rediscli.subscribe()
    templates = init_template()
    init_hostname_certname()
    push_config_to_redis(rediscli,templates)
    run(result)