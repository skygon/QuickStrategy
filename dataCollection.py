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
    def __init__(self, date_string):
        threading.Thread.__init__(self)
        self.date_string = date_string
        self.rtda = RTDA(date_string)
        self.start()

    def processOneCode(self, code):
        self.rtda.setCode(code)
        self.rtda.setParams(amount=20*100*100)
        count = self.rtda.getBillListCount()
        print count
        #data_summary = self.rtda.getBillListSummary()
        self.fetchDetails(count)
        #TODO write to redis
        

    
    def fetchDetails(self, count):
        pages = count / DEFAULT_PAGE_SIZE
        if count % DEFAULT_PAGE_SIZE > 0:
            pages = pages + 1
        
        for i in range(pages):
            self.rtda.setParams(amount=20*100*100, page=i+1)
            page_data = self.rtda.getBillList()
            print page_data


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


def getFullData(date_string):
    pass

def getRealTimeData(date_string):
    pass

if __name__ == "__main__":
    tdc = []
    for i in range(dc_thread_poll):
        tdc.append(DataCollection("2017-05-18"))

    for t in tdc:
        if t.isAlive():
            t.join()