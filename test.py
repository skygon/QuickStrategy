# -*- coding: utf8 -*-
import os
import json
from utils import *
from RedisOperator import RedisOperator

r = RedisOperator("localhost", 6379, 0)

def changeIndexToDict():
    l = r.llen('index_5')
    for i in range(l):
        s = r.lindex('index_5', i)
        data = json.loads(s)
        r.hset('index_5_dict', data['symbol'], s)


def prepareInfo():
    symbol = {}
    hkeys = r.hkeys('index_2_dict')
    print type(hkeys)
    for k in hkeys:
        symbol[k] = {}
        s = r.hget('index_2_dict', k)
        data = json.loads(s)
        symbol[k]['changepercent'] = data['changepercent']
        symbol[k]['turnoverratio'] = data['turnoverratio']
        symbol[k]['volume'] = data['volume']
        

def getTotalVolume():
    f = open('volume_info', 'w')
    hkeys = r.hkeys('index_2_dict')
    #print type(hkeys)
    for k in hkeys:
        s = r.hget('index_2_dict', k)
        data = json.loads(s)
        f.write(k)
        f.write(',')
        if data['turnoverratio'] == 0:
            f.write("0")
        else:
            total = int(data['volume'] / data['turnoverratio']) * 100
            f.write(str(total))
        f.write('\n')
    
    f.close()


if __name__ == '__main__':
    changeIndexToDict()
    #getTotalVolume()