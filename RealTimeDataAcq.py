import json
import urllib2

BILL_LIST = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?"
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
    
    def composeURL(self):
        url = BILL_LIST + "symbol=" + self.code
        for k, v in self.params_list.items():
            url = url + "&" + k + "=" + str(v)
        
        url = url + "&day=" + self.day
        print "url is %s" %(url)
        return url

    def getBillListCount(self):
        try:
        except Exception, e:
            print "getBillListCount error: %s \n" %(str(e))
    
    def getBillList(self):
        try:
            url = self.composeURL()
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            ret = response.getcode()
            if (ret != 200):
                raise Exception("response error")
            
            raw = response.read()
            text = raw.decode('gb2312')
            data = self.handleResponseBillList(text)
            json_data = json.loads(data)
            print json_data
        except Exception, e:
            print "getBillList error: %s \n" %(str(e))

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


if __name__ == "__main__":
    rtda = RTDA("2017-05-26")
    rtda.setCode("sh603993")
    rtda.setParams(amount=200*100*100, type=0)
    rtda.getBillList()
