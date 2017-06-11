#coding=utf-8

from sklearn.linear_model import LinearRegression 
import matplotlib.pyplot as plt 
from sklearn import metrics
import numpy as np 
import pandas as pd
import seaborn as sns

data = pd.read_csv('data.csv')
print data.head()
print data.shape

 
# visualize the relationship between the features and the response using scatterplots
sns.pairplot(data, x_vars=['TV','Radio','Newspaper'], y_vars='Sales', size=7, aspect=0.8)
plt.show()#注意必须加上这一句，否则无法显示。





