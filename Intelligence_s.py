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
    def __init__(self, day_index, volume_type):
        threading.Thread.__init__(self)
        self.k = 1.6
        self.big_deal_threshold = 0.15
        self.turnoverratio = 4
        self.prev_ku = 0
        self.prev_kd = 0 
        self.day_index = day_index
        self.volume_type = volume_type # small mid big
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
                self.weight[self.code] += self.analyzeKuKd(data, 5-i)
            
            table = "summary_" + str(self.day_index) + "_amount_0"
            s = self.redis.hget(table, self.code)
            if data is not None:
                data = json.loads(s)
                self.analyzeBigDealPer(data)
        except Exception, e:
            print "processOneCode error %s \n" %(str(e))

    def getCodeWeight(self, code):
        return self.weight[code]

    def sortWeight(self):
        # sort by value
        return sorted(self.weight.items(), key=operator.itemgetter(1), reverse=True)

    def calTurnoverRario(self, stockvol):
        totalvol = code_vol_map['sh'][self.volume_type][self.code]
        ratio = int(stockvol) / float(totalvol) * 100
        return ratio

    def analyzeBigDealPer(self, data):
        try:
            big_deal_per = float(data['totalvolpct'])
            if big_deal_per > 0.1 and big_deal_per < 0.3:
                self.weight[self.code] = self.weight[self.code] + 5
            else:
                self.weight[self.code] = self.weight[self.code] - 5
        except Exception,e:
            print "analyzeBigDealPer error %s \n" %(str(e))

    def analyzeKuKd(self, data, level):
        try:
            score = 0
            real_ku = int(data['kuvolume']) - self.prev_ku
            real_kd = int(data['kdvolume']) - self.prev_kd

            self.prev_ku += real_ku
            self.prev_kd += real_kd
            
            #ratio = self.calTurnoverRario(data['stockvol'])
            #big_deal_per = float(data['totalvolpct'])
            #alpha = big_deal_per / self.big_deal_threshold
            if real_ku > real_kd * 1.5:
            #if real_ku > real_kd * 0.7 and real_ku < real_kd * 1.2:
                score += level
            
            return score
        except Exception, e:
            print "analyzeKuKd error: %s \n" %(str(e))
            return 0

    
    def predictSH(self):
        for k in code_vol_map['sh'][self.volume_type].keys():
            self.code = k
            self.processOneCode()
        self.predict = self.sortWeight()
        #print self.predict

    def calPredictPrecision(self, real_rank, length):
        pt = 0
        pf = 0
        count = 0
        real_codes = [k[0] for k in real_rank][:length*3]
        predict_codes = [k[0] for k in self.predict][:length]
        
        for c in predict_codes:
            if count > length:
                break
            if c in real_codes:
                pt += 1
            else:
                pf += 1
            count += 1
        

        print "predict precision is %s" %(pt/float(pt+pf))


if __name__ == "__main__":
    volume_type = 'mid'
    myAI = MyAI(3, volume_type)
    myAI.predictSH()

    from trainning import Trainning
    t = Trainning(4,volume_type)
    t.getTrainningCode()

    myAI.calPredictPrecision(t.ranked, 20)


