# -*- coding: utf-8 -*-
import json
import urllib2

url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=20&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page"

request = urllib2.Request(url)

response = urllib2.urlopen(request)

info = response.info()
print info

data = response.read().decode('gb2312')
#print data

'''
{symbol:"sh600361",code:"600361",name:"华联综超",trade:"6.550",pricechange:"0.600",changepercent:"10.084",buy:"6.550",sell:"0.000",settlement:"5.950",open:"6.500",high:"6.550",low:"6.210",volume:31216149,amount:203406434,ticktime:"15:00:00",per:-16.795,pb:1.662,mktcap:436104.18629,nmc:436104.18629,turnoverratio:4.68846}
'''
def handleResponseStatus(data):
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

data = handleResponseStatus(data)

jdata = json.loads(data)
print type(jdata)

type(jdata[0]['changepercent'])
print jdata[0]['changepercent']





    
