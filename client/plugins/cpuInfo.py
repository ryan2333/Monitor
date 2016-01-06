#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import commands

def cpuInfo():
    shell_command = 'sar 1 3 |grep "^Average"'
    status, result = commands.getstatusoutput(shell_command)
    
    if status != 0:
        cpuDict = {'status': status}
    else: 
        user, nice, system, iowait, steal, idle = result.split()[2:]
        cpuDict = {
            '%user': user,
            '%nice': nice,
            '%system': system,
            '%iowait': iowait,
            '%steal': steal,
            '%idle': idle
            }
    return cpuDict