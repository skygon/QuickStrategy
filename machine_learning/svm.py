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
    def __init__(self, day_index, vol_type):
        self.day_index = day_index
        self.vol_type = vol_type
        self.svr_rbf = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
        self.svr_linear = svm.SVR(kernel='linear')
        self.svr_poly = svm.SVR(kernel='poly', C=1e3, degree=2)
        self.kernel_type = 'rbf'
        self.dp = DataPreparation(self.day_index, self.vol_type)
    
    
    def setKernel(self, kernel_type):
        self.kernel_type = kernel_type
    
    def getTrainningData(self, change_type='normal'):
        x, y = self.dp.generateTrainningData(change_type)
        print x.shape, y.shape
        return x, y
    
    def getTestData(self, change_type='normal'):
        x, y = self.dp.generateTestData(change_type)
        return x, y
    
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
    
    def fit(self):
        x, y = self.getTrainningData()
        #estimator = self.getEstimator()
        #self.svr_poly.fit(x, y.values.ravel())
        #estimator.fit(x, y.values.ravel())
        parameters = {'kernel':('rbf',), 'C':[1e3, 1e2, 1, 10]}
        svr = svm.SVR()
        self.estimator = GridSearchCV(svr, parameters)
        self.estimator.fit(x, y.values.ravel())

        print self.estimator


    def predict(self):
        x, real_y = self.getTestData()
        #estimator = self.getEstimator()
        #print estimator
        pred_y = self.estimator.predict(x)

        self.calcAllPrecision(real_y, pred_y)

        self.plotData(real_y, pred_y)
        
    
    def test(self):
        x, y = self.getTrainningData()

        parameters = {'kernel':('rbf',), 'C':[1e3, 1e2, 1, 10]}
        svr = svm.SVR()
        clf = GridSearchCV(svr, parameters)
        #clf = svm.SVR()
        clf.fit(x, y.values.ravel())

        #y_rbf = clf.fit(x, y.values.ravel()).predict(x)
        test_x, real_y = self.getTestData()
        pred_y = clf.predict(test_x)

        print "==== best estimator ======"
        print clf
        #print "==== checked cv results ===="
        #print clf.cv_results_
        self.calcAllPrecision(real_y, pred_y)

        print type(pred_y)
        print type(real_y.values)
        #print np.sort(pred_y)
        print np.sort(real_y.values, axis=None)
        
                
    

        

    

if __name__ == "__main__":
    mysvm = MySVM(1, 'small')
    mysvm.setKernel('rbf')
    mysvm.fit()
    mysvm.predict()
    #mysvm.test()
