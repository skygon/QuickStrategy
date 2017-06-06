import json
import operator
import threading
from Queue import Queue
from RedisOperator import RedisOperator
from utils import *

# weight
# For each level, if kuvolume >= k * kdvolume, weight add level+1, k should larger than 1.5. 
# All codes will be sorted by weight

class MyAI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.k = 1.6
        self.prev_ku = 0
        self.weight = {}
        self.redis = RedisOperator("localhost", 6379, 0)
        self.start()

    def processOneCode(self):
        self.weight[self.code] = 0
        for i in range(5):
            table = "summary_0_amount_" + str(4-i)
            data = self.redis.hget(table, self.code)
            if data is None:
                continue
            data = json.loads(data)
            print type(data)
            self.weight[self.code] += self.judgeData(data, 5-i)

    def sortWeight(self):
        # sort by value
        return sorted(self.weight.items(), key=operator.itemgetter(1), reverse=True)

    def judgeData(self, data, level):
        if self.prev_ku == data['kuvolume']:
            return 0
        
        self.prev_ku = data['kuvolume']
        if int(data['kuvolume']) >= int(data['kdvolume']) * self.k:
            return level

        return 0
    
    def run(self):
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
        for i in range(100):
            print result[i]


if __name__ == "__main__":
    myAI = MyAI()
