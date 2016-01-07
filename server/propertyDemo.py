#!/usr/bin/env python
#_*_coding:utf-8_*_

class Foo:
    def __init__(self):
        self.__dict = {'k1':2}
    @property   #使用装饰器在引用时可以不加括号，将私有字段当方法引用
    def Bar(self):
        return self.__dict
    
foo = Foo()
print foo.Bar