#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-06-17 10:59:56

#filter()也接收一个函数和一个序列。和map()不同的时，filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。
def f(x):
    return x % 2==1
L=filter(f,range(15))
print(list(L))
