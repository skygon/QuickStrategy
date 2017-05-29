# -*- coding: utf8 -*-
import os
from utils import *

def funcA(**kwargs):
    for k,v in kwargs.items():
        print type(k),type(v)


if __name__ == '__main__':
    funcA(price=4, name="sh000001")