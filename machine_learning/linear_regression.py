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
import seaborn as sns

