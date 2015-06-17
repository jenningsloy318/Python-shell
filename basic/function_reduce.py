#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-06-17 10:50:45
# reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
from functools import reduce
def f(x,y):
    return x*y
L=reduce(f,[2,3,4,5,6])
print(L)
