import json
import operator
import threading
import math
from Queue import Queue
from RedisOperator import RedisOperator
from utils import *
from plot import *

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

            if real_ku > real_kd * self.k:
                return level

            return 0
        except Exception, e:
            print "judgeData error: %s \n" %(str(e))
            return 0

    
    def predictSmallSH(self):
        for k in code_vol_map['sh']['small'].keys():
            self.code = k
            self.processOneCode()

if __name__ == "__main__":
    myAI = MyAI(3)
    myAI.predictSmallSH()
    print len(myAI.weight.keys())
    plotChangeIndexToKeyIndex(myAI.weight, 'b-*')
    from trainning import Trainning
    t = Trainning()
    t.getTrainningCode()

    plotChangeIndexToKeyIndex(t.sh_small, 'r-*')
    plt.show()

