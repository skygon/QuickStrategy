import os
import sys
import Queue
import threading
import json
from utils import *

# global variables
file_path = os.path.join(os.getcwd(), "detail_data")
SHA = os.path.join(os.getcwd(), "config", "sh_a.txt")
SZA = os.path.join(os.getcwd(), "config", "sz_a.txt")


thread_pool_num = 10
#analysis queue. Should be the all codes
analysis_queue = Queue.Queue()


#===============================Helper functions========================================
def usage():
    print '''
    usage:
    python detailAnalysis.py date_string
    example : python detailAnalysis.py "2017-05-18"
    '''

def read_to_queue(prefix, file_name):
    f = open(file_name)
    line = f.readline()
    while line:
        if isInvalidCode(line.strip('\n')): # there are some stocks with total volumn 0
            continue
        code = prefix + line.strip('\n')
        analysis_queue.put(code)
        line = f.readline()
    f.close()

def init_analysis_queue():
    analysis_queue.put("sh600010")
    # read codes from files
    #read_to_queue('sh', SHA)
    #read_to_queue('sz', SZA)

def compose_filename(code):
    fn = code + ".csv"
    full_path = os.path.join(file_path, fn)
    mylogger("full path %s", full_path)
    return full_path


def mylogger(message, vars):
    print message %(vars)
#===============================End of helper functions=================================


class Analyzer(threading.Thread):
    def __init__(self, date_string):
        threading.Thread.__init__(self)
        self.date_string = date_string
        self.data = {}
        self.big_deal_amount = {}
        self.big_deal_volume = {}
        self.initDataStruct()
        self.start()

    def initDataStruct(self):
        self.data.clear()
        self.data['time'] = []
        self.data['price'] = []
        self.data['volume'] = []
        self.data['type'] = []

        self.big_deal_amount.clear() #We have five levels
        for i in range(DEAL_LEVEL):
            self.big_deal_amount[i] = {}
            self.big_deal_amount[i]['time'] = []
            self.big_deal_amount[i]['price'] = []
            self.big_deal_amount[i]['volume'] = []
            self.big_deal_amount[i]['type'] = []

        self.big_deal_volume.clear()
        # TODO

    
    def dumpToFile(self):
        try:
            f = open('output.json', 'wb')
            json.dump(self.data, f)
        except Exception, e:
            print "ERROR-dumpFile: %s\n" %str(e)
        finally:
            f.close()



    def writeToDatabase(self, data):
        pass
    
    #line format: time price diff volumn amount type
    def processOneLine(self, line):
        s = line.strip('\n').split('\t')
        self.data['time'].append(s[0])
        self.data['price'].append(float(s[1]))
        self.data['volume'].append(int(s[3]))
        #print repr(s[5])
        if repr(s[5]) == repr(BUY_STR):
            self.data['type'].append(DealType.BUY)
        elif repr(s[5]) == repr(SELL_STR):
            self.data['type'].append(DealType.SELL)
        else:
            self.data['type'].append(DealType.UNKNOW)
    
    def parseFile(self, file_path):
        try:
            mylogger("file path %s", file_path)
            f = open(file_path)
            line = f.readline()
            line = f.readline() #skip title line
            while line:
                self.processOneLine(line)
                line = f.readline()
            self.dumpToFile()
        except Exception, e:
            print "parseFile failed: %s \n" %str(e)
        finally:
            f.close()

    def getBigDealByAmount(self, level):
        try:
            for i in range(len(self.data['time'])):
                if self.data['volume'][i] * self.data['price'][i] * 100 > BIG_DEAL['amount'][level]:
                    print "current: ", self.data['volume'][i] * self.data['price'][i] * 100
                    self.big_deal_amount[level]['time'].append(self.data['time'][i])
                    self.big_deal_amount[level]['price'].append(self.data['price'][i])
                    self.big_deal_amount[level]['volume'].append(self.data['volume'][i])
                    self.big_deal_amount[level]['type'].append(self.data['type'][i])
            print self.big_deal_amount[level]
        except Exception, e:
            print "getBigDealByAmount error %s \n" %str(e)

    def doAnalysis(self):
        try:
            # Deal level analysis
            for i in range(DEAL_LEVEL):
                self.getBigDealByAmount(i)
            print self.big_deal_amount
        except Exception, e:
            print "doAnalysis error %s \n" %str(e)
        

    def run(self):
        while True:
            try:
                self.initDataStruct()
                code = analysis_queue.get(False) 
                mylogger("I got code: %s \n", code)
                file_path = compose_filename(code)
                self.parseFile(file_path)
                self.doAnalysis()
            except Queue.Empty:
                print "All works have been completed \n"
                break
            except Exception, e:
                print "ERROR: analysis failed %s\n" %str(e)


def here_we_go(date_string):
    init_analysis_queue()
    threads = []
    for i in range(thread_pool_num):
        threads.append(Analyzer(date_string))

    for t in threads:
        if t.isAlive():
            t.join()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)
    
    here_we_go(sys.argv[1])

    

