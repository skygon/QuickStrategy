# -*- coding: utf8 -*-
import os

f = open('E:\sh603993.csv')

line = f.readline()
while line:
    print line
    line = f.readline()

f.close()