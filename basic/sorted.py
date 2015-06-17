#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Jennings Liu@ 2015-06-17 10:08:11

sort_tuple=[('acbd',15,'male'),('ccc',22,'female'),('dfd',17,'male')]
sort_result=sorted(sort_tuple,key=lambda student: student[1]) #lambda 定义一个单行函数.
print(sort_result)
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
L_result1=sorted(L,key=lambda scores:scores[1],reverse=True)
print(L_result1)
L_result2=sorted(L,key=lambda scores:scores[0])
print(L_result2)

