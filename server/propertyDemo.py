#!/usr/bin/env python
#_*_coding:utf-8_*_

class Foo:
    def __init__(self):
        self.__dict = {'k1':2}
    @property   #ʹ��װ����������ʱ���Բ������ţ���˽���ֶε���������
    def Bar(self):
        return self.__dict
    
foo = Foo()
print foo.Bar