#!/usr/bin/env python
#coding:utf-8

import redis

class RedisHelper:
    
    def __init__(self):
        self.__conn = redis.Redis(host='127.0.0.1')
        
    
    def get(self,key):
        return self.__conn.get(key)
    
    def set(self,key,value):
        self.__conn.set(key, value)
    '''  
    def set_ex(self,key,value,ex):
        self.__conn.set(key,value,ex)
    '''
        
    def public(self,msg):
        self.__conn.publish('FM90.0', msg) 
        
    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe('FM90.0')
        pub.parse_response()
        return pub
    