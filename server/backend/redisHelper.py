#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import redis
from time import sleep
class RedisHelper:
    def __init__(self):
        self.__conn = redis.Redis(host='127.0.0.1', port=6379)
    
    def get(self,key):
        return self.__conn.get(key)
    
    def set(self, key, value):
        self.__conn.set(key, value)
    
    def fabu(self, channel, msg):
        self.__conn.publish('FM90.0', msg) 
        
    def subscribe(self,):
        pub = self.__conn.pubsub()
        pub.subscribe('FM90.0')
        pub.parse_response()
        return pub


