#!/usr/bin/env python
#_*_coding:utf-8_*_
from backend.redisHelper import *
import json

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
    def editCpu(self):
        return self.Items
    
def init_template():
    t1 = BaseTemplate(cpu=DefaultCpuMonitor(), mem=DefaultMemMonitor(),load=DefaultLoadMonitor())
    return {'template1': t1}   

    
cpu = BaseMonitor('cpu', 10, 'getCpuInfo', 0, {'idle':75})
mem = BaseMonitor('mem', 10, 'getMemInfo', 0, {'MemAvailable':1500000})
load = BaseMonitor('load', 10, 'getLoadInfo', 0, {'load5':[0.02, 0.1]})

template1 = BaseTemplate(cpu, mem, load)
