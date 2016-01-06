#!/usr/bin/env python
#_*_ coding:utf-8 _*_


import commands
def loadInfo():   
    shell_command = 'uptime'
    
    status,result = commands.getstatusoutput(shell_command)
    
    if status != 0:
        loadDic = { 'status': status }
    else:
        uptime = " ".join(result.split()[:-7][1:])
        load1, load5, load15 = result.split('average:')[1].split(',')
        loadDic = {
            'uptime': uptime,
            'load1': load1,
            'load5': load5,
            'load15': load15,
            'status': status
            }

    return loadDic