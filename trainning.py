import json
import operator
from utils import *
from RedisOperator import RedisOperator


class Trainning(object):
    def __init__(self):
        # get redis connection
        self.redis= RedisOperator('localhost',6379,0)
        # sh small rank
        self.sh_small = {} # code <-> changepercent
        self.getTrainningCode()
    
    def getTrainningCode(self):
        for k in code_vol_map['sh']['small'].keys():
            s = self.redis.hget('index_4_dict', k)
            if s is None:
                continue
            data = json.loads(s)
            self.sh_small[k] = float(data['changepercent'])

            #ranked =  sorted(sh_small.items(), key=operator.itemgetter(1), reverse=True)
            #print ranked

    
