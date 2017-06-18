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
STEP = 6 # 6 days

class DataPreparation(object):
    def __init__(self, day_index, vol_type):
        self.day_index = day_index
        self.vol_type = vol_type # small, mid, big
        self.big_deal_type = 0 # 0 - 4
        self.factors = ['ku'] #factors are all from summary table

        self.summary_table = "summary_" + str(self.day_index) + "_amount_" + str(self.big_deal_type)
        self.index_table = "index_" + str(self.day_index+1) + "_dict"
        self.test_summary_table = "summary_" + str(self.day_index+1) + "_amount_" + str(self.big_deal_type)
        self.validate_index_table = "index_" + str(self.day_index+2) + "_dict"

        self.x_keys = ['kukd', 'bigdealvolpct', 'turnoverratio'] # TODO add more futures, like RSI, MACD, KDJ ...
        self.y_keys = ['score']
        self.data_source = [] 

        self.redis = RedisOperator('localhost', 6379, 0)

    def generateTrainningData(self, change_type='normal'):
        return self.generateData(self.summary_table, self.index_table, change_type)

    def generateTestData(self, change_type='normal'):
        return self.generateData(self.test_summary_table, self.validate_index_table, change_type)
    
    # STEP (6) days average data 
    def generateRawData(self, change_type='normal'):
        data_source = []
        (tku, tkd, inc, dec, bigvolpct) = (0,0,0,0,0)

        for k in code_vol_map['sh'][self.vol_type].keys():
            for day in range(self.day_index+1 - STEP, self.day_index+1):
                summary_table = "summary_" + str(day) + "_amount_" + str(self.big_deal_type)
                index_table = "index_" + str(day) + "_dict"
                s = self.redis.hget(summary_table, k)
                rs = self.redis.hget(index_table, k)
                if s is None or rs is None:
                    continue
                
                 # futures from big deal summary
                data = json.loads(s)
                e = {}
                tku += int(data['kuvolume'])
                tkd += int(data['kdvolume'])
                bigvolpct += float(data['totalvolpct']) * 100




    def generateData(self, summary_table, index_table, change_type):
        data_source = []
        for k in code_vol_map['sh'][self.vol_type].keys():
            s = self.redis.hget(summary_table, k)
            rs = self.redis.hget(index_table, k)
            if s is None or rs is None:
                continue
            
            # futures from big deal summary
            data = json.loads(s)
            e = {}
            ku = int(data['kuvolume'])
            kd = int(data['kdvolume'])

            if ku == 0 and kd ==0:
                kukd = 0
            elif ku == 0:
                kukd = 0.1
            elif kd == 0:
                kukd = 10
            else:
                kukd = float(ku) / float(kd) * 5
            
            e['kukd'] = kukd
            e['bigdealvolpct'] = float(data['totalvolpct']) * 100
            # cal change vol percent
            stockvol = float(data['stockvol'])
            e['turnoverratio'] = stockvol / code_vol_map['sh'][self.vol_type][k] * 100
            
            # target from index
            index_data = json.loads(rs)
            cp = float(index_data['changepercent'])
            score = 0
            if change_type == 'normal':
                score = self.transChange2Score(cp)
            elif change_type == 'class':
                score = self.transChange2Catalog(cp)
            
            e['score'] = score
            data_source.append(e)
            # trans cp to score

        #trainning data x
        df = pd.DataFrame.from_records(data_source)
        x = df[self.x_keys]
        y = df[self.y_keys]

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


if __name__ == "__main__":
    dp = DataPreparation(7, 'small')
    x, y = dp.generateTrainningData()
    print x.head(20)