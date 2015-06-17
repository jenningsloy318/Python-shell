#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-06-17 10:41:25

def f(x):
    return x**4
print(list(map(f,[1,2,3,4,5]))) #map函数有两个参数，第一个是函数(只能接收一个参数的函数)，第二个是个list序列，map函数作用是将第一个序列的每一个参数放入一个个参数中执行，获得所有序列的结果
