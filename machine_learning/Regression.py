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
from sklearn.linear_model.logistic import  LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.cross_validation import train_test_split  #这里是引用了交叉验证
import matplotlib.pyplot as plt 
from sklearn import metrics
import numpy as np 
import pandas as pd
#import seaborn as sns

# trainning :       day_index  -> day_index+1
# predict testing:  day_inde+1 -> day_index+2
class Prediction(object):
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

    def linearRegression(self):
        x, y = self.generateTrainningData(self.summary_table, self.index_table)
        self.linreg = LinearRegression()
        model = self.linreg.fit(x, y)
        print model # LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
        print self.linreg.intercept_ # 2.87696662232
        #print self.linreg.coef_ # [ 0.04656457  0.17915812  0.00345046]
        r = zip(self.x_keys, self.linreg.coef_[0])
        print r
    
    def testLinearPrecision(self):
        x, real_y = self.generateTrainningData(self.test_summary_table, self.validate_index_table)
        _, previous_y = self.generateTrainningData(self.summary_table, self.index_table)
        predict_y = self.linreg.predict(x)

        # RMSE
        sum_mean = 0
        for i in range(len(predict_y)):
            sum_mean += (predict_y[i] - real_y.values[i])**2
        sum_erro = np.sqrt(sum_mean / len(predict_y))
        print "RMSE: %s" %(sum_erro)
        

        pos = 0
        neg = 0

        for i in range(len(predict_y)):
            if float(predict_y[i]) > 0 and float(real_y.values[i][0]) < 0:
                neg += 1
            else:
                pos += 1
            
            
        
        print "Predict precison is %s" %(pos / float(pos+neg))

        # plot lines
        plt.figure()
        plt.grid(True)
        plt.plot(range(len(predict_y)), predict_y,'b-o',label="predict")
        plt.plot(range(len(real_y)), real_y,'r-*',label="real")
       # plt.plot(range(len(previous_y)), previous_y,'ys',label="previous")
        plt.show()
        
        
    def logisticRegression_fake(self):
        raw_train_x, raw_train_y = self.generateTrainningData(self.summary_table, self.index_table)
        raw_test_x, raw_real_y = self.generateTrainningData(self.test_summary_table, self.validate_index_table)

        self.logisticReg = LogisticRegression()

        '''# TD-IDF 算法获取特征向量
        vectorizer = TfidfVectorizer()
        train_x = vectorizer.fit_transform(raw_train_x)
        test_x = vectorizer.transform(raw_test_x)
        '''
        print raw_train_x.shape
        print raw_train_y.shape


        y = []
        for i in range(len(raw_train_y)/2):
            y.append(1)
            y.append(0)
        #print y
        #train_y = 1 / (1 + np.e ** (-train_y)) 
        #print raw_train_y.values
        #train_y = [1 / (1 + np.e ** (-y)) for y in raw_train_y.values[0]]
        #print train_y
        #plt.plot(raw_train_y.values, train_y, 'r')
        self.logisticReg.fit(raw_train_x, y)
    
    def sigmod(self, raw):
        r = []
        x = []
        for i in range(len(raw)):
            #print raw.values[i][0]
            f = 1 / (1 + np.e ** (-raw.values[i][0]))
            if f > 0.5:
                r.append(1)
            else:
                r.append(0)
        #print r
        return r

    def logisticRegression(self):
        train_x, raw_train_y = self.generateTrainningData(self.summary_table, self.index_table)
        self.logisticReg = LogisticRegression()

        train_y = self.sigmod(raw_train_y)
        self.logisticReg.fit(train_x, train_y)
    
    def testLogisticRegression(self):
        test_x, raw_real_y = self.generateTrainningData(self.test_summary_table, self.validate_index_table)
        real_y = self.sigmod(raw_real_y)
        predict_y = self.logisticReg.predict(test_x)
        print type(predict_y)
        print np.mean(predict_y == real_y)

        pos = 0
        neg = 0
        for i in range(len(predict_y)):
            if int(predict_y[i] == real_y[i]):
                pos += 1
            else:
                neg += 1
        
        print "Predict precision is %s " %(pos / float(pos+neg))



    def generateTrainningData(self, summary_table, index_table):
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
            score = self.transChange2Score(cp)
            #score = cp
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
        else:
            score = int(cp)
        return score

    

if __name__ == "__main__":
    lp = Prediction(3, 'small')
    lp.linearRegression()
    lp.testLinearPrecision()
    #lp.logisticRegression()
    #lp.testLogisticRegression()

            




