
# -*- coding: utf-8 -*-
import urllib2
import json

url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?symbol=sh603993&num=60&page=1&sort=ticktime&asc=0&volume=0&amount=2000000&type=0&day=2017-05-26"
request = urllib2.Request(url)

response = urllib2.urlopen(request)

print response.getcode()
print response.geturl()
res = response.read()

print response.info() 
'''
response.info() 是非常有用的函数。能得到很多请求相关的信息
Server: Sina
Date: Sun, 28 May 2017 07:11:37 GMT
Content-Type: text/plain; charset=gb2312
Content-Length: 1141
Connection: close
Set-Cookie: U_TRS1=00000075.81cc1689.592a7829.a901b144; path=/; expires=Wed, 26-May-27 07:11:37 GMT;
 domain=.sina.com.cn
Set-Cookie: U_TRS2=00000075.81d91689.592a7829.32e32b13; path=/; domain=.sina.com.cn
Cache-Control: max-age=10
Expires: Sun, 28 May 2017 07:11:47 GMT
Last-Modified: Sun, 28 May 2017 07:11:37 GMT
DPOOL_HEADER: hrand137
Vary: Accept-Encoding
Set-Cookie: FINANCE2=0707fb184bb5b670efd548a344c055e3;Path=/
DPOOL_LB7_HEADER: hrand115
POOLPOOL4: finance2
'''

y = res.decode('gb2312')
print type(y)

y = y.replace('symbol', '"symbol"')
y = y.replace('name', '"name"')
z = y.replace('ticktime', '"ticktime"')
#z = y.replace('price', '"price"')
z = z.replace('volume', '"volume"')
z = z.replace('prev_price', '"xxxxx"')
z = z.replace('kind', '"kind"')
z = z.replace('price', '"price"')

print z

'''
ValueError: Expecting property name enclosed in double quotes: line 1 column 3 (char 2)
python 的json格式字符串，key必须在双引号之内
s = '[{"symbol":"sh603993","name":"洛阳钼业","ticktime":"14:58:40","price":"4.230","volume":"182600","prev_price":"4.230","kind":"U"},{"symbol":"sh603993","name":"洛阳钼业","ticktime":"14:58:40","price":"4.230","volume":"182600","prev_price":"4.230","kind":"U"}]'
x = s.decode('utf-8')
#print x
y = json.loads(x)
print type(y)
print y
'''

s = json.loads(z)
print s[0]['symbol']





