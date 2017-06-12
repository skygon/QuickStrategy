#coding=utf-8

# system libs
import os
import sys
p = os.path.join(os.getcwd())
sys.path.append(p)

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

class LinearPredict(object):
    def __init__(self, day_index):
        self.day_index = day_index
        self.factors = ['ku'] #factors are all from summary table
        self.redis = RedisOperator('localhost', 6379, 0)

    def generateTrainningData(self)


