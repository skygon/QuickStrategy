import threading
import Queue
from RealTimeDataAcq import RTDA
from utils import *

'''
3000+ stocks data collection, include deal details and current day's stutation.
Use queue and multithreading to fetch real time/ current day's full data.
Full data is used for machine learning.
Real time data for making quick strategy.
'''
dc_thread_poll = 2
test_queue = Queue.Queue()
test_queue.put("sh603993")
for_debug = True

class DataCollection(threading.Thread):
    '''
    judge: by default, amount. Currently, volume is not supported
    data_type: bill_list, bill_list_summary, stocks_index
    level: 0 - 4.
    '''
    def __init__(self, data_type, level, date_string):
        threading.Thread.__init__(self)
        self.data_type = data_type
        self.level = level
        self.date_string = date_string
        self.rtda = RTDA(date_string)
        self.start()

    def processOneCode(self, code):
        self.rtda.setCode(code)
        self.rtda.setParams(amount=BIG_DEAL['amount'][self.level])
        if self.data_type == 'bill_list':
            self.getBillList()
        elif self.data_type == 'bill_list_summary':
            self.getBillListSummary()
        elif self.data_type == 'stocks_index':
            self.getStocksIndex()
        

    def getStocksIndex(self):
        pass

    def getBillListSummary(self):
        pass

    def getBillList(self):
        pass
    
    def fetchByPage(self, page, data_type):
        self.rtda.setParams(amount=BIG_DEAL['amount'][self.level], page=i+1)
        if data_type == 'bill_list':
            page_data = self.rtda.getBillList()
        elif data_type == 'stocks_index':
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
        tdc.append(DataCollection("2017-05-18"))

    for t in tdc:
        if t.isAlive():
            t.join()
