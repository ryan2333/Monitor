#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import loadInfo, cpuInfo, memoryInfo

def getLoadInfo():
    return loadInfo.loadInfo()

def getCpuInfo():
    return cpuInfo.cpuInfo()

def getMemInfo():
    return memoryInfo.memInfo()