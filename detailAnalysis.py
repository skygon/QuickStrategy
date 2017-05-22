import os
import Queue
import threading
from utils import *

# global variables
file_path = os.path.join(os.getcwd(), "detail_data")
SHA = os.path.join(os.getcwd(), "config", "sh_a.txt")
SZA = os.path.join(os.getcwd(), "config", "sz_a.txt")

BUY_STR = '\xe4\xb9\xb0\xe7\x9b\x98'
SELL_STR = '\xe5\x8d\x96\xe7\x9b\x98'

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
        code = prefix + line.strip('\n')
        analysis_queue.put(code)
        line = f.readline()
    f.close()

def init_analysis_queue():
    # read codes from files
    read_to_queue('sh', SHA)
    read_to_queue('sz', SZA)

def compose_filename(code):
    fn = code + ".csv"
    return os.path.join(file_path, fn)


def mylogger(message, vars):
    print message %(vars)
#===============================End of helper functions=================================


class Worker(threading.Thread):
    def __init__(self, date_string):
        treading.Thread.__init__(self)
        self.date_string = date_string
        self.data = {}
        initDataStruct()

    def initDataStruct(self):
        self.data.clear()
        self.data['time'] = []
        self.data['price'] = []
        self.data['volume'] = []
        self.data['type'] = []
    
    def writeToDatabase(self, data):
        pass
    
    def processOneLine(self, line):
        pass
    
    def doAnalysis(self, file_path):
        f = open(file_path)
        line = f.readline()
        while line:
            processOneLine(line)
            line = f.readline()
        f.close()

    def run(self):
        while True:
            try:
                code = analysis_queue.get(False) 
                mylogger("I got code: %s \n", code)
                file_path = compose_filename(code)
                doAnalysis(file_path)
            except Queue.Empty:
                print "All works have been completed"
            except Exception:
                print "ERROR: analysis failed"
