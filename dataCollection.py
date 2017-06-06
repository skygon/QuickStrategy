import threading
import Queue
from RealTimeDataAcq import RTDA
from RedisOperator import RedisOperator
from utils import *

'''
3000+ stocks data collection, include deal details and current day's stutation.
Use queue and multithreading to fetch real time/ current day's full data.
Full data is used for machine learning.
Real time data for making quick strategy.
'''
dc_thread_poll = 300
test_queue = Queue.Queue()
test_queue.put("sh603993")
for_debug = False

# redis storage structuer
# summary index table
# |
# == key     : TABLE_SUMMARY
# == field1  : day_index. 
# == value1  : day index. 0, 1, 2, ...
# == field2  : sort_type
# == value2  : amount or volume
# == field3  : level
# == value3  : 0 - 4
# So the real data table of summary is TABLE_SUMMARY_dayIndex_dataType_level. For example summary_0_amount_1, 0th day, sort by amount and
#  level is 1.

# summary data table
# |
# == key : summary_0_amount_0 summary_0_amount_1 ...
# == field <-> code
# == value  : json format string

class DataCollection(threading.Thread):
    '''
    judge: by default, amount. Currently, volume is not supported
    data_type: bill, index
    api_type: bill_list, bill_list_summary, stocks_index
    level: 0 - 4.
    '''
    def __init__(self, data_type, api_type, level, date_string):
        threading.Thread.__init__(self)
        self.data_type = data_type # used for params
        self.api_type = api_type
        self.level = level
        self.date_string = date_string
        self.rtda = RTDA(date_string)
        self.redis = RedisOperator("localhost", 6379, 0)
        # add table index to redis
        self.addTableIndex()
        self.start()


    def addTableIndex(self):
        table = redis_conf['name'][self.api_type]

        self.redis.hset(table, 'day_index', 0)
        self.redis.hset(table, 'sort_type', 'amount')
        self.redis.hset(table, 'level', self.level)

        self.data_table = table + "_" + str(0) + '_amount_' + str(self.level)
    

    def processOneCode(self, code):
        self.code = code
        self.rtda.setCode(code)
        self.rtda.setParams(self.data_type, amount=BIG_DEAL['amount'][self.level])
        if self.api_type == 'bill_list':
            self.getBillList()
        elif self.api_type == 'bill_list_summary':
            self.getBillListSummary()
        elif self.api_type == 'stocks_index':
            self.getStocksIndex()
        

    def getStocksIndex(self):
        pass

    def getBillListSummary(self):
        data = self.rtda.getBillListSummary()[0] # return one element array
        self.redis.hsetJson(self.data_table, self.code, data)
        print "Write to redis for %s" %(self.data_table)


    def getBillList(self):
        pass
    
    def fetchByPage(self, page, api_type):
        self.rtda.setParams(amount=BIG_DEAL['amount'][self.level], page=i+1)
        if api_type == 'bill_list':
            page_data = self.rtda.getBillList()
        elif api_type == 'stocks_index':
            page_data = self.rtda.getStocksIndex()
        
        return page_data


    def run(self):
        while True:
            try:
                if for_debug:
                    code = test_queue.get(False)
                else:
                    code = code_queue.get(False)
                print "I got code %s \n" %(code)
                self.processOneCode(code)
            except Queue.Empty:
                print "All works of DataCollection have been done \n"
                break
            except Exception, e:
                print "DataCollection Error : %s \n" %(str(e))





if __name__ == "__main__":
    tdc = []
    for i in range(dc_thread_poll):
        tdc.append(DataCollection('bill', 'bill_list_summary', 4, '2017-06-05'))

    for t in tdc:
        if t.isAlive():
            t.join()
