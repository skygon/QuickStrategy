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

    def fit(self):
        x, y = self.getTrainningData()
        estimator = self.getEstimator()
        #self.svr_poly.fit(x, y.values.ravel())
        estimator.fit(x, y.values.ravel())
        print estimator


    def predict(self):
        x, real_y = self.getTestData()
        #x, real_y = self.getTrainningData()
        estimator = self.getEstimator()
        print estimator
        pred_y = estimator.predict(x)

        pos = 0
        neg = 0
        for i in range(len(real_y)):
            if pred_y[i] > 0 and real_y.values[i][0] < 0:
                neg += 1
            else:
                print pred_y[i], real_y.values[i][0]
                pos += 1
            
        print "Estimator precision is %s " %(float(pos) / float(pos + neg))
                

        '''
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
        '''
        
    
    def test(self):
        x, y = self.getTrainningData('class')

        #parameters = {'kernel':('poly', 'rbf'), 'C':[1e3, 1e2, 1, 10]}
        #svr = svm.SVR()
        #clf = GridSearchCV(svr, parameters)
        clf = svm.SVC()
        clf.fit(x, y.values.ravel())

        #y_rbf = clf.fit(x, y.values.ravel()).predict(x)
        x, y = self.getTestData('class')
        y_rbf = clf.predict(x)

        print "==== best estimator ======"
        print clf
        #print "==== checked cv results ===="
        #print clf.cv_results_

        #plt.scatter(range(len(y)), y, 'k', label='data')
        plt.figure()
        plt.plot(range(len(y)), y, 'r-v', label='data')
        plt.plot(range(len(y)), y_rbf, 'g-o', label='estimate')
        #plt.plot(X, y_lin, c='r', label='Linear model')
        #plt.plot(X, y_poly, c='b', label='Polynomial model')
        plt.xlabel('data')
        plt.ylabel('target')
        plt.title('Support Vector Regression')
        plt.legend()
        plt.show()
    

        

    

if __name__ == "__main__":
    mysvm = MySVM(6, 'small')
    mysvm.setKernel('rbf')
    mysvm.fit()
    mysvm.predict()
    #mysvm.test()
