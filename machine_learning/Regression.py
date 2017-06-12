#coding=utf-8

# system libs
import os
import sys
p = os.path.join(os.getcwd())
sys.path.append(p)
import json

# native quickstrategy lib
from utils import *
from trainning import Trainning
from RedisOperator import RedisOperator

# machine learning related libs
from sklearn.linear_model import LinearRegression
#from sklearn.cross_validation import train_test_split  #这里是引用了交叉验证
import matplotlib.pyplot as plt 
from sklearn import metrics
import numpy as np 
import pandas as pd
#import seaborn as sns

# trainning :       day_index  -> day_index+1
# predict testing:  day_inde+1 -> day_index+2
class LinearPredict(object):
    def __init__(self, day_index):
        self.day_index = day_index
        self.factors = ['ku'] #factors are all from summary table
        self.summary_table = "summary_" + str(self.day_index) + "_amount_0"
        self.index_table = "index_" + str(self.day_index+1) + "_dict"
        self.x_keys = ['kuvolume', 'kdvolume', 'totalvolpct', 'changevolpct']
        self.y_keys = ['score']
        self.keys = ['kuvolume', 'kdvolume', 'totalvolpct'] #changevolpct is derived from both table
        self.data_source = [] # structure: kuvolume, kdvolume, totalvolpct, changevolpct, score
        
        self.redis = RedisOperator('localhost', 6379, 0)

    def 
    def generateTrainningData(self):
        for k in code_vol_map['sh']['small'].keys():
            s = self.redis.hget(self.summary_table, k)
            rs = self.redis.hget(self.index_table, k)
            if s is None or rs is None:
                continue
            data = json.loads(s)
            e = {}
            for t in self.keys:
                e[t] = data[t]
            # cal change vol percent
            stockvol = float(data['stockvol'])
            e['changevolpct'] = stockvol / code_vol_map['sh']['small'][k] * 100
            
            data = json.loads(rs)
            cp = float(data['changepercent'])
            score = self.transChange2Score(cp)
            e['score'] = score
            self.data_source.append(e)
            # trans cp to score

        #trainning data x
        self.df = pd.DataFrame.from_records(self.data_source)
        self.x = self.df[self.x_keys]
        self.y = self.df[self.y_keys]
        print "X:"
        print self.x.shape
        print self.x.head()
        print "Y:"
        print self.y.shape
        print self.y.head()
    
    def transChange2Score(self, cp):
        score = 0
        if cp >= 10.0:
            score = 10.0
        elif cp >= 7.0:
            score = 9.0
        elif cp >= 5.0:
            score = 7.0
        elif cp >= 2.0:
            score = 5.0
        elif cp >= 1.0:
            score = 2.0
        else:
            score = 0
        return score

    

if __name__ == "__main__":
    lp = LinearPredict(2)
    lp.generateTrainningData()

            




