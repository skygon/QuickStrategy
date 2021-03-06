import numpy as np
from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

# Generate sample data
x = np.sort(5 * np.random.rand(40, 1), axis=0)
y = np.sin(x).ravel()

###############################################################################
# Add noise to targets
y[::5] += 3 * (0.5 - np.random.rand(8))

###############################################################################
# Fit regression model
'''
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(X, y).predict(X)
y_lin = svr_lin.fit(X, y).predict(X)
y_poly = svr_poly.fit(X, y).predict(X)
'''

parameters = {'kernel':('linear', 'poly', 'rbf'), 'C':[1e3, 1e2, 1, 10], 'degree': [2, 3]}
svr = svm.SVR()
clf = GridSearchCV(svr, parameters)
y_rbf = clf.fit(x, y).predict(x)

print "==== best estimator ======"
print clf
print "==== checked cv results ===="
print clf.cv_results_

###############################################################################
# look at the results
plt.scatter(x, y, c='k', label='data')
plt.hold('on')
plt.plot(x, y_rbf, c='g', label='RBF model')
#plt.plot(X, y_lin, c='r', label='Linear model')
#plt.plot(X, y_poly, c='b', label='Polynomial model')
plt.xlabel('data')
plt.ylabel('target')
plt.title('Support Vector Regression')
plt.legend()
plt.show()