import redis
import sys
import json
sys.path.append('E:\mywork\QuickStrategy')
#sys.path.append('/Users/yuncui/Documents/QuickStrategy')
from RealTimeDataAcq import RTDA
from RedisOperator import RedisOperator
from utils import *

'''
https://pypi.python.org/pypi/redis/2.10.5
'''

def handleResponseStocksIndex(data):
    data = data.replace('symbol', '"symbol"')
    data = data.replace('code', '"code"')
    data = data.replace('name', '"name"')
    data = data.replace('trade', '"trade"')
    data = data.replace('pricechange', '"pricechange"')
    #side affect
    data = data.replace('per', '"per"')
    data = data.replace('change"per"cent', '"changepercent"')
    data = data.replace('buy', '"buy"')
    data = data.replace('sell', '"sell"')
    data = data.replace('settlement', '"settlement"')
    data = data.replace('open', '"open"')
    data = data.replace('high', '"high"')
    data = data.replace('low', '"low"')
    data = data.replace('volume', '"volume"')
    data = data.replace('amount', '"amount"')
    data = data.replace('ticktime', '"ticktime"')
    data = data.replace('pb', '"pb"')
    data = data.replace('mktcap', '"mktcap"')
    data = data.replace('nmc', '"nmc"')
    data = data.replace('turnoverratio', '"turnoverratio"')
    return data

r = RedisOperator("localhost", 6379, 0)

data = r.lindex('index_2', 3)
print data

