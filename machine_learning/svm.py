# coding=utf-8
import os
import sys
sys.path.append(os.getcwd())
from utils import *
from DataPreparation import DataPreparation
import numpy as np
from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

# sklearn libs
# GBDT>=SVM>=RF>=Adaboost
# There are three different implementations of Support Vector Regression:
#  SVR, NuSVR and LinearSVR

from sklearn import svm

class MySVM(object):
    def __init__(self):
        self.svr_rbf = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
        self.svr_linear = svm.SVR(kernel='linear')
        self.svr_poly = svm.SVR(kernel='poly', C=1e3, degree=2)
        self.kernel_type = 'rbf'
    
    
    def setKernel(self, kernel_type):
        self.kernel_type = kernel_type
    
    
    def getEstimator(self):
        if self.kernel_type == 'rbf':
            return self.svr_rbf
        elif self.kernel_type == 'linear':
            return self.svr_linear
        elif self.kernel_type == 'poly':
            return self.svr_poly
        else:
            raise Exception("Unsuppoerted kernel type")
    
    def calcTopPrecision(self, real_y, pred_y, size):
        pass
    def calcAllPrecision(self, real_y, pred_y):
        pos = 0
        neg = 0
        for i in range(len(real_y)):
            if pred_y[i] > 0 and real_y.values[i][0] < 0:
                neg += 1
            elif pred_y[i] < 0 and real_y.values[i][0] >= 2:
                neg += 1
            else:
                pos += 1
            
        print "Estimator precision is %s " %(float(pos) / float(pos + neg))
    
    def plotData(self, real_y, pred_y):
        plt.figure()
        plt.plot(range(len(real_y)), real_y, 'k-*', label='data')
        plt.plot(range(len(real_y)), pred_y, 'g-o', label='RBF model')
        #plt.plot(X, y_lin, c='r', label='Linear model')
        #plt.plot(X, y_poly, c='b', label='Polynomial model')
        plt.xlabel('data')
        plt.ylabel('target')
        plt.title('Support Vector Regression')
        plt.legend()
        plt.show()
    
    def fit(self, x, y):
        parameters = {'kernel':('rbf',), 'C':[1e3, 1e2, 1, 10]}
        svr = svm.SVR()
        self.estimator = GridSearchCV(svr, parameters)
        self.estimator.fit(x, y.values.ravel())

        print self.estimator


    def predict(self, x, real_y):
        pred_y = self.estimator.predict(x)
        self.plotData(real_y, pred_y)
        

if __name__ == "__main__":
    mysvm = MySVM()
    # trainning
    dp = DataPreparation(7, 'mid')
    x, y = dp.generateData()
    print "=====fit===="
    mysvm.fit(x, y)

    # predict
    dp = DataPreparation(8, 'mid')
    x, y = dp.generateData()
    print "=====predict===="
    mysvm.predict(x, y)
