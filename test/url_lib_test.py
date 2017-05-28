
# -*- coding: utf8 -*-
import urllib2
import json

url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?symbol=sh603993&num=60&page=1&sort=ticktime&asc=0&volume=0&amount=200000&type=0&day=2017-05-26"
request = urllib2.Request(url)

response = urllib2.urlopen(request)

print response.getcode()
print response.geturl()
res = response.read()

print type(res)

print res[0]

rres = repr(res)

dres = json.dumps(rres)

print type(dres)

x = json.loads(dres)

print type(x)



ss = "{'a': 1, 'b':2}"
z = json.loads(ss)

