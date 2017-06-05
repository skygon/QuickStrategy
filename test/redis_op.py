import redis
import sys
import json
sys.path.append('E:\mywork\QuickStrategy')
from RealTimeDataAcq import RTDA

'''
https://pypi.python.org/pypi/redis/2.10.5
'''

r = redis.Redis(host='localhost', port=6379, db=0)

rtda = RTDA("2017-05-26")
rtda.setCode("sh603993")

#rtda.setParams('bill', amount=200*100*100, type=0)
#data = rtda.getBillListSummary()

# test summary api
rtda.setParams('index', num=20)
data = rtda.getStocksIndex()
print len(data)

r.hset('index', 0, json.dumps(data[0]))

d = r.hget('index', 0)
print d

jd = json.loads(d)
print type(jd)
