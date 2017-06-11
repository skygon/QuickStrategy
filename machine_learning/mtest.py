#coding=utf-8
import os
from sklearn.linear_model import LinearRegression
#from sklearn.cross_validation import train_test_split  #这里是引用了交叉验证
import matplotlib.pyplot as plt 
from sklearn import metrics
import numpy as np 
import pandas as pd
import seaborn as sns

fn = os.path.join(os.getcwd(), 'machine_learning', 'data.csv')
data = pd.read_csv(fn)
print data.head()
print data.shape

 
# visualize the relationship between the features and the response using scatterplots
# seaborn的pairplot函数绘制X的每一维度和对应Y的散点图。通过设置size和aspect参数来调节显示的大小和比例。
sns.pairplot(data, x_vars=['TV','Radio','Newspaper'], y_vars='Sales', size=7, aspect=0.8)
#plt.show()

# 通过加入一个参数kind='reg'，seaborn可以添加一条最佳拟合直线和95%的置信带。
sns.pairplot(data, x_vars=['TV','Radio','Newspaper'], y_vars='Sales', size=7, aspect=0.8, kind='reg')
#plt.show()

# 多元线性回归模型
# y=β0+β1∗TV+β2∗Radio+...+βn∗Newspape

'''
scikit-learn要求X是一个特征矩阵，y是一个NumPy向量。
pandas构建在NumPy之上。
因此，X可以是pandas的DataFrame，y可以是pandas的Series，scikit-learn可以理解这种结构。
'''
#create a python list of feature names
feature_cols = ['TV', 'Radio', 'Newspaper']
# use the list to select a subset of the original DataFrame
X = data[feature_cols]
# equivalent command to do this in one line
X = data[['TV', 'Radio', 'Newspaper']]
# print the first 5 rows
print X.head()
# check the type and shape of X
print type(X)
print X.shape

# select a Series from the DataFrame
y = data['Sales']
# equivalent command that works if there are no spaces in the column name
y = data.Sales
# print the first 5 values
print type(y)
print y.head()

# 构建训练集和测试集. NOTE： 可以自己定义函数来构造训练集和测试集
'''
X_train,X_test, y_train, y_test = train_test_split(X, y, random_state=1)
# 默认75%是训练集，25%是测试集
print X_train.shape
print y_train.shape
print X_test.shape
print y_test.shape
'''
def train_test_split(ylabel, random_state=1):
    import random 
    index=random.sample(range(len(ylabel)),50*random_state)
    list_train=[]
    list_test=[]
    i=0
    for s in range(len(ylabel)):
        if i in index:
            list_test.append(i)
        else:
            list_train.append(i)
        i+=1
    return list_train,list_test


 ###############对特征进行分割#############################
feature_cols = ['TV', 'Radio','Newspaper']
X1 = data[feature_cols]
y1 = data.Sales
list_train,list_test=train_test_split(y1)#random_state的默认值是1

X_train=X1.ix[list_train] #这里使用来DataFrame的ix（）函数，可以将指定list中的索引的记录全部放在一起
X_test=X1.ix[list_test]
y_train=y1.ix[list_train]
y_test=y1.ix[list_test]


# 线性回归
linreg = LinearRegression()
model=linreg.fit(X_train, y_train)
print model # LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
print linreg.intercept_ # 2.87696662232
print linreg.coef_ # [ 0.04656457  0.17915812  0.00345046]

# pair the feature names with the coefficients
r = zip(feature_cols, linreg.coef_)
print r
# output:
# [('TV', 0.04656456787415026), ('Radio', 0.17915812245088847), ('Newspaper', -0.0034504647111804625)]
# that is : y = 2.877+0.0466∗TV+0.179∗Radio-0.00345∗Newspaper

# test， 预测
y_pred = linreg.predict(X_test)

# Compare y_pred and y_test
'''
这里介绍3种常用的针对线性回归的测度。
(1)平均绝对误差(Mean Absolute Error, MAE)
(2)均方误差(Mean Squared Error, MSE)
(3)均方根误差(Root Mean Squared Error, RMSE)
'''

# RMSE
print type(y_pred),type(y_test)
print len(y_pred),len(y_test)
print y_pred.shape,y_test.shape

sum_mean=0
for i in range(len(y_pred)):
    sum_mean+=(y_pred[i]-y_test.values[i])**2
sum_erro=np.sqrt(sum_mean/50)
# calculate RMSE by hand
print "RMSE by hand:",sum_erro

# ROC line
plt.figure()
plt.plot(range(len(y_pred)),y_pred,'b',label="predict")
plt.plot(range(len(y_pred)),y_test,'r',label="test")
plt.legend(loc="upper right") #显示图中的标签
plt.xlabel("the number of sales")
plt.ylabel('value of sales')
plt.show()


