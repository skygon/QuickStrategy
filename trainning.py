import json
import operator
from utils import *
from plot import *
from RedisOperator import RedisOperator


class Trainning(object):
    def __init__(self, day_index):
        self.day_index = day_index
        # get redis connection
        self.redis= RedisOperator('localhost',6379,0)
        # sh small rank
        self.sh_small = {} # code <-> changepercent
        self.index_dict = "index_" + str(self.day_index) + "_dict"
    
    def getTrainningCode(self):
        for k in code_vol_map['sh']['small'].keys():
            s = self.redis.hget(self.index_dict, k)
            if s is None:
                continue
            data = json.loads(s)
            self.sh_small[k] = float(data['changepercent'])
            self.ranked =  sorted(self.sh_small.items(), key=operator.itemgetter(1), reverse=True)
            #print ranked


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    t = Trainning()
    t.getTrainningCode()

    plotChangeIndexToKeyIndex(t.sh_small, 'r-*')
    
    
