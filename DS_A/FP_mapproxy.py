"""
types模块，引入了一个封装类名MappingProxyType
接收一个映射作为参数，返回一个只读的映射视图
该视图是动态的，对原映射做出改变时，可以通过试图观察到
"""
from types import MappingProxyType


d = {1: 'A'}
d_proxy = MappingProxyType(d)
print(d_proxy)
print(d_proxy[1])
# print(d_proxy[2])

d[2] = 'B'
print(d_proxy[2])