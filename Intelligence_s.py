import json
import operator
import threading
import math
from Queue import Queue
from RedisOperator import RedisOperator
from utils import *

# weight
# For each level, if kuvolume >= k * kdvolume, weight add level+1. How to set value of k is a key point
# All codes will be sorted by weight

class MyAI(threading.Thread):
    def __init__(self, day_index):
        threading.Thread.__init__(self)
        self.k = 1.6
        self.turnoverratio = 4
        self.prev_ku = 0
        self.prev_kd = 0 
        self.day_index = day_index
        # add turnoverratio from index
        self.weight = {}
        self.symbol = {}
        self.redis = RedisOperator("localhost", 6379, 0)
        # day index used to predict stocks trending
        self.index_dict = "index_" + str(self.day_index + 1) + "_dict"
        self.start()

    def prepareInfo(self):
        hkeys = self.redis.hkeys(self.index_dict)
        #print type(hkeys)
        for k in hkeys:
            self.symbol[k] = {}
            s = self.redis.hget(self.index_dict, k)
            data = json.loads(s)
            self.symbol[k]['changepercent'] = float(data['changepercent'])
            self.symbol[k]['turnoverratio'] = float(data['turnoverratio'])
            self.symbol[k]['volume'] = int(data['volume'])
        #print self.symbol["sh600074"]

    # real time turnoverratio should be get from summary['stockvol']
    def RealTimePrepareInfo(self):
        pass

    def processOneCode(self):
        try:
            self.weight[self.code] = 0
            for i in range(5):
                table = "summary_" + str(self.day_index) + "_amount_" + str(4-i)
                data = self.redis.hget(table, self.code)
                if data is None:
                    continue
                data = json.loads(data)
                #print type(data)
                self.weight[self.code] += self.judgeData(data, 5-i)
        except Exception, e:
            print "processOneCode error %s \n" %(str(e))

    def getCodeWeight(self, code):
        return self.weight[code]

    def sortWeight(self):
        # sort by value
        return sorted(self.weight.items(), key=operator.itemgetter(1), reverse=True)

    def judgeData(self, data, level):
        try:
            real_ku = int(data['kuvolume']) - self.prev_ku
            real_kd = int(data['kdvolume']) - self.prev_kd

            self.prev_ku += real_ku
            self.prev_kd += real_kd

            # a is used to find how big is the big bill
            a = float(data['totalvolpct']) / 0.5 
            if self.symbol[self.code]['turnoverratio'] > 30:
                return 0 # currently, don't take care of turn over ratio bigger than 15%
            if real_ku > real_kd * self.k:
                return level * math.pow(a, 2) * self.symbol[self.code]['turnoverratio']/self.turnoverratio

            return 0
        except Exception, e:
            print "judgeData error: %s \n" %(str(e))
            return 0
    
    def run(self):
        self.prepareInfo()
        while True:
            try:
                self.code = code_queue.get(False)
                self.processOneCode()
            except Queue.Empty:
                print "All works done \n"
                break
            except Exception, e:
                print "Ohh, MyAI has some problem... %s\n" %(str(e))
        
        # result 
        result = self.sortWeight()
        for i in range(50):
            print result[i]


if __name__ == "__main__":
    myAI = MyAI(1)
