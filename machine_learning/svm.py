# coding=utf-8
import os
import sys
sys.path.append(os.getcwd())
from utils import *
from DataPreparation import DataPreparation

# sklearn libs
from sklearn import svm

x = [[0, 0], [2, 2]]
y = [0.5, 2.5]

clf = svm.SVR()
clf.fit(x, y)

print clf