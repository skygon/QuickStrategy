# -*-coding:utf-8 -*-
# 
# Created on 2017-04-10, by skygon
 
import requests
import time
import sys
import threading

from Queue import Queue
from optparse import OptionParser

#itchat, a weixin autoreply tool
import itchat, time
from itchat.content import *

#when should pusher send msg to weixin account
#TODO put this obj into a configuration file.
threshold = {}
threshold['s_sh603993'] = {}
threshold['s_sz000897'] = {}

#s_sh603993 洛阳钼业
threshold['s_sh603993']['lower'] = 4.5
threshold['s_sh603993']['middle'] = 4.7
threshold['s_sh603993']['upper'] = 4.9

#s_sz000897 津滨发展
threshold['s_sz000897']['lower'] = 6.2
threshold['s_sz000897']['middle'] = 6.3
threshold['s_sz000897']['upper'] = 6.4


#global queue
pusherQueue = Queue()
#TODO list:
#1. Add Receiver. Which can receive customer's new stock request. Using itchat's auto reply. Need another working thread 
#on listening coming message.
#2. log to file

class Pusher(threading.Thread):
    """Stock information push to weixin account"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = {}
        self.init_status()
    
    def init_status(self):
        for k in threshold.keys():
            self.status[k] = ""

    def info_warning(self, sid, curValue):
        msg = "Current value of " + str(sid) + " : " + str(curValue)
        itchat.send_msg(msg, "filehelper")

    def strong_warning(self, sid, curValue):
        msg = "[WARNING!!!]Current value of " + str(sid) + " : " + str(curValue)
        itchat.send_msg(msg, "filehelper")

    def quick_strategy(self, sid, curValue, strategyTable):
        if curValue <= strategyTable['lower'] and self.status[sid] != "lower": #lower only inform when status changes
            self.status[sid] = "lower"
            self.strong_warning(sid, curValue)
        elif curValue <= strategyTable['middle'] and self.status[sid] != "lower_middle":  #lower_middle only inform when status changes
            self.status[sid] = "lower_middle"
            self.info_warning(sid, curValue)
        elif curValue <= strategyTable['upper'] and self.status[sid] != "middle_upper": #middle_upper only inform when status changes
            self.status[sid] = "middle_upper"
            self.info_warning(sid, curValue)
        elif curValue > strategyTable['upper']: #always inform when current share's value is bigger than upper threshold
            self.status[sid] = "upper"
            self.strong_warning(sid, curValue)
        

    def run(self):
        itchat.auto_login(True) #login weixin

        while True:
            #current in format (0, 's_sz000897', '6.47')
            current = pusherQueue.get()
            sid = current[1]
            value = float(current[2])
            if sid in threshold:
                self.quick_strategy(sid, value, threshold[sid])



class Worker(threading.Thread):
    """多线程获取"""
    def __init__(self, work_queue, result_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()

    def run(self):
        while True:
            func, arg, code_index = self.work_queue.get()
            res = func(arg, code_index)
            self.result_queue.put(res)
            if self.result_queue.full():
                #res format: [(0, 's_sz000897', '6.47'), (1, 's_sh603993', '5.010')]
                res = sorted([self.result_queue.get() for i in range(self.result_queue.qsize())], key=lambda s: s[0], reverse=False)
                print '***** start *****'
                for obj in res:
                    pusherQueue.put(obj)
                    print obj
                print '***** end *****\n'
            self.work_queue.task_done()


class Stock(object):
    """股票实时价格获取"""

    def __init__(self, code, thread_num):
        self.code = code
        self.work_queue = Queue()
        self.threads = []
        self.__init_thread_poll(thread_num)

    def __init_thread_poll(self, thread_num):
        self.params = self.code.split(',')
        #self.params.extend(['s_sh000001', 's_sz399001'])  # 默认获取沪指、深指
        self.result_queue = Queue(maxsize=len(self.params[::-1]))
        for i in range(thread_num):
            self.threads.append(Worker(self.work_queue, self.result_queue))

    def __add_work(self, stock_code, code_index):
        self.work_queue.put((self.value_get, stock_code, code_index))

    def del_params(self):
        for obj in self.params:
            self.__add_work(obj, self.params.index(obj))

    def wait_all_complete(self):
        for thread in self.threads:
            if thread.isAlive():
                thread.join()

    @classmethod
    def value_get(cls, code, code_index):
        #slice_num, value_num = 21, 3
        slice_num, value_num = 23, 1
        name, now = u'——无——', u'  ——无——'
        if code in ['s_sh000001', 's_sz399001']:
            slice_num = 23
            value_num = 1
        r = requests.get("http://hq.sinajs.cn/list=%s" % (code,))
        print r.text.encode("utf-8")
        res = r.text.encode("utf-8").split(',')
        if len(res) > 1:
            #name, now = res[0][slice_num:], res[value_num]
            name, now = code, res[value_num]
        return code_index, name ,  now


if __name__ == '__main__':
    parser = OptionParser(description="Query the stock's value.", usage="%prog [-c] [-s] [-t]", version="%prog 1.0")
    parser.add_option('-c', '--stock-code', dest='codes',
                      help="the stock's code that you want to query.")
    parser.add_option('-s', '--sleep-time', dest='sleep_time', default=6, type="int",
                      help='How long does it take to check one more time.')
    parser.add_option('-t', '--thread-num', dest='thread_num', default=3, type='int',
                      help="thread num.")
    options, args = parser.parse_args(args=sys.argv[1:])

    assert options.codes, "Please enter the stock code!"  # 是否输入股票代码
    print options.codes.split(',')
    if filter(lambda s: s[:-6] not in ('sh', 'sz', 's_sh', 's_sz'), options.codes.split(',')):  # 股票代码输入是否正确
        raise ValueError

    stock = Stock(options.codes, options.thread_num)

    #start pusher
    pusher = Pusher()
    pusher.start()

    while True:
        print "start to get information..."
        stock.del_params()
        time.sleep(options.sleep_time)