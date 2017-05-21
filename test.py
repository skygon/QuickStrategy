# -*- coding: utf8 -*-
import os

f = open('E:\skygon\QuickStrategy\detail_data\sh600010.csv')

count = 0

line = f.readline()
while line:
    print line
    print line.strip('\n').split('\t')
    line = f.readline()
    count += 1
    if count > 10:
        break

f.close()