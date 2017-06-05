import redis
import sys
import json
#sys.path.append('E:\mywork\QuickStrategy')
sys.path.append('/Users/yuncui/Documents/QuickStrategy')
from RealTimeDataAcq import RTDA
from RedisOperator import RedisOperator
from utils import *

'''
https://pypi.python.org/pypi/redis/2.10.5
'''

r = RedisOperator("localhost", 6379, 0)
rtda = RTDA("2017-06-05")
rtda.setParams('index', num=20)
data = rtda.getStocksIndex()

for i in range(len(data)):
    r.hsetJson(INDEX, i, data[i])


for i in range(r.hlen(INDEX)):
    s = r.hget(INDEX, i)
    print json.dumps(s)