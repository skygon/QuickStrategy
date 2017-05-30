import json
import urllib2

BILL_LIST = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?"
BILL_LIST_COUNT = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillListCount?"
BILL_LIST_SUMMARY = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillSum?"

#example url:
#http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?symbol=sh603993&num=60&page=1&sort=ticktime&asc=0&volume=0&amount=200000&type=0&day=2017-05-26

class RTDA(object):
    def __init__(self, date_string):
        self.day = date_string
        # params day must as the last item
        self.params_list = {}
        self.initParamsList()
        
    def initParamsList(self):
        self.params_list['num'] = 60
        self.params_list['page'] = 1 #first page
        self.params_list['sort'] = "ticktime"
        self.params_list['asc'] = 0
        self.params_list['volume'] = 0 # By default, use amount mode
        self.params_list['type'] = 0
        # change the following params
        #self.params_list['symbol'] = "change_me"
        self.params_list['amount'] = 50 * 100 * 100
        #self.params_list['day'] = "1970-01-01"
    
    def setCode(self, code):
        self.code = code

    def setParams(self, **kwargs):
        for k, v in kwargs.items():
            self.params_list[k] = v
    
    def composeURL(self, bill_type):
        url = ""
        if bill_type == "bill_list":
            url = BILL_LIST + "symbol=" + self.code
        elif bill_type == "bill_list_count":
            url = BILL_LIST_COUNT + "symbol=" + self.code
        elif bill_type == "bill_list_summary":
            url = BILL_LIST_SUMMARY + "symbol=" + self.code
        else:
            raise Exception("composeURL error. Unsupported bill type")
        for k, v in self.params_list.items():
            url = url + "&" + k + "=" + str(v)
        
        url = url + "&day=" + self.day
        print "url is %s" %(url)
        return url

    def getRawData(self, bill_type):
        url = self.composeURL(bill_type)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        ret = response.getcode()
        if (ret != 200):
            raise Exception("response error")
        
        raw = response.read()
        text = raw.decode('gb2312') #codec is from response.info()
        return text

    def getBillListCount(self):
        try:
            text = self.getRawData("bill_list_count")
            return int(text[13:-3]) # (new String("10"))
        except Exception, e:
            print "getBillListCount error: %s \n" %(str(e))

    def getBillList(self):
        try:
            text = self.getRawData("bill_list")
            data = self.handleResponseBillList(text)
            return json.loads(data)
        except Exception, e:
            print "getBillList error: %s \n" %(str(e))

    def getBillListSummary(self):
        try:
            text = self.getRawData("bill_list_summary")
            data = self.handleResponseSummary(text)
            return json.loads(data)
        except Exception, e:
            print "getBillListSummary error : %s \n" %(str(e))

    def handleResponseBillList(self, data):
        data = data.replace('symbol', '"symbol"')
        data = data.replace('name', '"name"')
        data = data.replace('ticktime', '"ticktime"')
        #z = y.replace('price', '"price"')
        data = data.replace('volume', '"volume"')
        data = data.replace('prev_price', '"prev"')
        data = data.replace('kind', '"kind"')
        data = data.replace('price', '"price"')
        #print "data is: \n"
        #print data
        return data
    
    
    def handleResponseSummary(self, data):
        data = data.replace('symbol', '"symbol"')
        data = data.replace('name', '"name"')
        data = data.replace('opendate', '"opendate"')
        data = data.replace('minvol', '"minvol"')
        data = data.replace('voltype', '"voltype"')
        
        #Be careful here. totalvolpct actually will be "totalvol"pct
        data = data.replace('totalvol', '"totalvol"')
        data = data.replace('"totalvol"pct', '"totalvolpct"')
        
        data = data.replace('totalamt', '"totalamt"')
        data = data.replace('"totalamt"pct', '"totalamtpct"')
        
        data = data.replace('avgprice', '"avgprice"')
        data = data.replace('kuvolume', '"kuvolume"')
        data = data.replace('kuamount', '"kuamount"')
        data = data.replace('kevolume', '"kevolume"')
        data = data.replace('keamount', '"keamount"')
        data = data.replace('kdvolume', '"kdvolume"')
        data = data.replace('kdamount', '"kdamount"')
        data = data.replace('stockvol', '"stockvol"')
        data = data.replace('stockamt', '"stockamt"')
        #print data
        return data


if __name__ == "__main__":
    rtda = RTDA("2017-05-26")
    rtda.setCode("sh603993")
    rtda.setParams(amount=200*100*100, type=0)
    data = rtda.getBillListSummary()
    print data

