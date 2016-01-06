#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import commands

def memInfo():
    shell_command = "grep -Ei '^(Mem|buffers|swap|cache)' /proc/meminfo"
    status, result = commands.getstatusoutput(shell_command)
    
    if status != 0:
        memDict = {'status':status}
    else:
        memDict = {}
        for i in result.split("\n"):
            k, v = i.split(":")
            memDict[k] = v.strip()
        memDict['status'] = status
        return memDict
