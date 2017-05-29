import json
import urllib2

BILL_LIST = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?"
#example url:
#http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?symbol=sh603993&num=60&page=1&sort=ticktime&asc=0&volume=0&amount=200000&type=0&day=2017-05-26

class RTDA(object):
    def __init__(self, code):
        self.code = code
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
        for k, v in kwargs:
            self.params_list[k] = v
    
    def composeURL(self):
        for k, v in self.params_list.items():


    def getBillList(self):


    
    