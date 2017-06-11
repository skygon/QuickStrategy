import json
import operator
from utils import *
from plot import *
from RedisOperator import RedisOperator


class Trainning(object):
    def __init__(self, day_index, volume_type):
        self.day_index = day_index
        self.volume_type = volume_type
        # get redis connection
        self.redis= RedisOperator('localhost',6379,0)
        # sh small rank
        self.sh_small = {} # code <-> changepercent
        self.index_dict = "index_" + str(self.day_index) + "_dict"
    
    def getTrainningCode(self):
        for k in code_vol_map['sh'][self.volume_type].keys():
            s = self.redis.hget(self.index_dict, k)
            if s is None:
                continue
            data = json.loads(s)
            self.sh_small[k] = float(data['changepercent'])
            self.ranked =  sorted(self.sh_small.items(), key=operator.itemgetter(1), reverse=True)
            #print ranked
        
    def writeToRedis(self):
        table = "trainning_" + self.volume_type
        for k in self.ranked:
            code = k[0]
            s = self.redis.hget(self.index_dict, code)
            self.redis.rpush(table, s)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    t = Trainning(4, 'mid')
    t.getTrainningCode()
    t.writeToRedis()
    #t.getTrainningCode()

    #plotChangeIndexToKeyIndex(t.sh_small, 'r-*')
    
    
