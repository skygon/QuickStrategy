# coding=utf-8
import os
import sys
p = os.path.join(os.getcwd())
sys.path.append(p)
import json

# native quickstrategy lib
from utils import *
from trainning import Trainning
from RedisOperator import RedisOperator

#machine learn related libs
import numpy as np 
import pandas as pd

# GBDT (Gradient Boost Decision Tree, 梯度提升决策树) 
# SVM

class WorkSpace(object):
     def __init__(self, day_index, vol_type):
        self.day_index = day_index
        self.vol_type = vol_type # small, mid, big
        self.big_deal_type = 0 # 0 - 4
        self.factors = ['ku'] #factors are all from summary table

        self.summary_table = "summary_" + str(self.day_index) + "_amount_" + str(self.big_deal_type)
        self.index_table = "index_" + str(self.day_index+1) + "_dict"
        self.test_summary_table = "summary_" + str(self.day_index+1) + "_amount_" + str(self.big_deal_type)
        self.validate_index_table = "index_" + str(self.day_index+2) + "_dict"

        self.x_keys = ['kuvolume', 'kdvolume', 'totalvolpct', 'changevolpct']
        self.y_keys = ['score']
        self.keys = ['kuvolume', 'kdvolume', 'totalvolpct'] #changevolpct is derived from both table
        self.data_source = [] # structure: kuvolume, kdvolume, totalvolpct, changevolpct, score
        
        self.redis = RedisOperator('localhost', 6379, 0)

    def generateTrainningData(self, summary_table, index_table, change_type='normal'):
        data_source = []
        for k in code_vol_map['sh'][self.vol_type].keys():
            s = self.redis.hget(summary_table, k)
            rs = self.redis.hget(index_table, k)
            if s is None or rs is None:
                continue
            data = json.loads(s)
            e = {}
            for t in self.keys:
                e[t] = data[t]
            # cal change vol percent
            stockvol = float(data['stockvol'])
            e['changevolpct'] = stockvol / code_vol_map['sh'][self.vol_type][k] * 100
            
            data = json.loads(rs)
            cp = float(data['changepercent'])
            score = 0
            if change_type == 'normal':
                score = self.transChange2Score(cp)
            elif change_type == 'LDA':
                score = self.transChange2Catalog(cp)
            
            e['score'] = score
            data_source.append(e)
            # trans cp to score

        #trainning data x
        df = pd.DataFrame.from_records(data_source)
        x = df[self.x_keys]
        y = df[self.y_keys]
        '''
        print "X:"
        print type(x)
        print x.shape
        print x.head()
        print "Y:"
        print type(y)
        print y.shape
        print y.head()
        '''
        return x,y
    
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
        elif cp > 0:
            score = 0
        elif cp > -2.0:
            score = -2.0
        elif cp > -5.0:
            score = -5.0
        else:
            score = -10.0
        return score

    def transChange2Catalog(self, cp):
        score = 0
        if cp > 5.0:
            score = 5
        elif cp > 0:
            score = 3
        else:
            score = 0
        return score
