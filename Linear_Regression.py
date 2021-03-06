# -*- coding: utf-8 -*-
"""ML_HW1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qLLIg-2ZXG5hE7CmUdCVMN1P4uOEPgh_
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso

"""Dataset loading and visualising using .head() function"""

data=pd.read_csv('/content/drive/MyDrive/abalone.csv')

"""Adding a constant coulmn in the data"""

data['W0']=1
data.head()

"""data visualisation"""
N=len(data)
data.info()

data.describe()

"""We now need to hot encode all the coulmns of data which contains text"""

"""Hot encoding of "Sex" coulmn"""
import numpy as np
M = [-1]*N
F = [-1]*N
I = [-1]*N
columnName='Sex'
for i in range (N):
    if(data[columnName][i]=='M'):
      M[i]=1
      F[i]=0
      I[i]=0
    elif(data[columnName][i]=='F'):
      M[i]=0
      F[i]=1
      I[i]=0   
    elif(data[columnName][i]=='I'):
      M[i]=0
      F[i]=0
      I[i]=1
data["M"]=M
data["F"]=F
data["I"]=I
data=data.drop(['Sex'],axis=1)

"""data visualisation after hot encoding"""
data.head()

"""Randomising the data to be use"""
random=np.random.RandomState(seed=42).permutation(len(data))
data=data.iloc[random]

x=data.drop(['Rings'],axis=1)
y=data['Rings']

"""Function for spliting data into train and test set"""
def test_train_splt(n,k,r):
  train=[]
  test=[]
  for i in range(n):
    if (i>=int((k-1)*r*n) and i<=int(k*r*n)):
      test.append(i)
    else:
      train.append(i)
  return train,test

"""Simple linear regression function without any regularisation"""
class LinearRegression() :
      
    def __init__( self, learning_rate, iterations ) :
          
        self.learning_rate = learning_rate
        self.iterations = iterations          
    def fit( self, X, Y ) :
          
        self.m, self.n = X.shape
        self.W = np.zeros( self.n )
  
        self.X = X
        self.Y = Y         
        for i in range( self.iterations ) :
          self.gradients = 2/self.m *(self.X.T).dot(self.X.dot(self.W) -self.Y)
          self.W=self.W-self.learning_rate*self.gradients
        return self

    def predict( self, X ) :    
        return X.dot( self.W )

from math import *
"""Function for calculation of Root mean square error"""
def RMSE(X,Y):
  sub=np.array(X)-np.array(Y)
  return sqrt(sum(sub**2)/len(sub))

"""I have tried the linear regression on these learning rate but got good results on 0.3"""
#learning_rate=[0.0003,0.001,0.003,0.01,0.03,0.1,0.3]
learning_rate=0.3
r=0.2
n=len(x)
iter=[]
mean_rmse_test=[]
mean_rmse_train=[]
min_rmse=100
min_rmse_k=-1
for number_of_iter in range(0,1000,100):
  m_rmse_test=0
  m_rmse_train=0
  for k in range(1,6):
    model = LinearRegression(learning_rate,number_of_iter)
    train_ind,test_ind=test_train_splt(n,k,r)
    x_train, y_train=x.iloc[train_ind],y.iloc[train_ind]
    x_test, y_test=x.iloc[test_ind],y.iloc[test_ind]
    model.fit(x_train, y_train)
    Y_train_p = model.predict(x_train)
    Y_test_p=model.predict(x_test)
    #print(sqrt(mean_squared_error(Y_train_p,y_train)),sqrt(mean_squared_error(Y_test_p,y_test)))
    train_rmse=RMSE(Y_train_p,y_train)
    test_rmse=RMSE(Y_test_p,y_test)
    m_rmse_test+=test_rmse
    m_rmse_train+=train_rmse
    if(test_rmse<min_rmse):
      min_rmse=test_rmse
      min_rmse_k=k
  mean_rmse_test.append(m_rmse_test/5)
  mean_rmse_train.append(m_rmse_train/5)
  iter.append(number_of_iter)

print("mean ramse on validation set:" ,mean_rmse_test)
print("mean ramse on train set:" ,mean_rmse_train)

"""Ploting figure required for the first part"""


plt.plot(iter,mean_rmse_test,'-r')
plt.title("mean_rmse_validation")
plt.xlabel('Number of Iterartions')
plt.ylabel("Mean_RMSE")

plt.show()

plt.plot(iter,mean_rmse_train,'-b')
plt.xlabel('Number of Iterartions')
plt.ylabel("Mean_RMSE")
plt.title("mean_rmse_train")

plt.show()

plt.plot(iter,mean_rmse_test,label="Validation RMSE")
plt.plot(iter,mean_rmse_train,label="Train RMSE")
plt.xlabel('Number of Iterartions')
plt.ylabel("Mean_RMSE")
plt.title("Combined Plot of Validation and Train RMSE")
plt.legend()
plt.show()

"""In this Block of code i have implemented linear regression using normal method(Matrix multiplication method)"""
rmse_test=[]
rmse_train=[]
for k in range(1,6):
    train_ind,test_ind=test_train_splt(n,k,r)
    x_train, y_train=x.iloc[train_ind],y.iloc[train_ind]
    x_test, y_test=x.iloc[test_ind],y.iloc[test_ind]
    theta_best = np.linalg.pinv(x_train).dot(y_train)
    #print(theta_best)
    y_pred_test=x_test.dot(theta_best)
    y_pred_train=x_train.dot(theta_best)
    rmse_test.append(RMSE(y_pred_test,y_test))
    rmse_train.append(RMSE(y_pred_train,y_train))


print("rmse on Validation set: ",rmse_test)
print("rmse on train set: ",rmse_train)

print("mean_rmse on Validation set: ",sum(rmse_test)/5)
print("mean_rmse on train set: ",sum(rmse_train)/5)

""" Quest1 part B """

"""splitting traing and testing set according to best error found on validation set in part a)"""
tra_ind,tes_ind=test_train_splt(n,3,r)
x_tra, y_tra=x.iloc[tra_ind],y.iloc[tra_ind]
x_tes, y_tes=x.iloc[tes_ind],y.iloc[tes_ind]

"""Regularised Linear Model"""
class Regularised_LinearRegression() :
      
    def __init__( self, learning_rate, iterations,alpha) :
          
        self.learning_rate = learning_rate
        self.iterations = iterations 
        self.alpha=alpha
        
    def fit_L1( self, X, Y ) :
          
        self.m, self.n = X.shape
        self.W = np.zeros( self.n )
  
        self.X = X
        self.Y = Y         
        for i in range( self.iterations ) :
          self.W_temp=np.zeros(self.n)
          for i in range(self.n):
            if(self.W[i]>0):
              self.W_temp[i]=1
            elif(self.W[i]==0):
              self.W_temp[i]=0
            else:
              self.W_temp[i]=-1
        
          self.gradients = (2/self.m * self.X.T.dot(self.X.dot(self.W) - self.Y))+(self.alpha*self.W_temp)
          self.W=self.W-self.learning_rate*self.gradients
        return self

    def fit_L2( self, X, Y ) :
          
        self.m, self.n = X.shape
        self.W = np.zeros( self.n )
  
        self.X = X
        self.Y = Y         
        for i in range( self.iterations ) :
          self.gradients = 2/self.m * self.X.T.dot(self.X.dot(self.W) - self.Y)+(self.alpha*self.W)
          self.W=self.W-self.learning_rate*self.gradients
        
        return self

    def predict( self, X ) :    
        return X.dot( self.W )

"""Hyper parameter tunning for L2"""


ridge=Ridge()
param={'alpha':[1e-10,1e-5,1e-3,1e-2,1e-1,0.3,0.8,1,10,100,1000]}
ridge_regressor=GridSearchCV(ridge,param,scoring="neg_root_mean_squared_error", cv=5)
ridge_regressor.fit(x_tra,y_tra)

alpha=ridge_regressor.best_params_['alpha']
print("Best hyperparameter for L2 case is:",alpha)

"""Using L2 regularised linear model for prediction"""
iter_L2=[]
reg_rmse_test_L2=[]
reg_rmse_train_L2=[]

for number_of_iter in range(0,3000,300):
    model =Regularised_LinearRegression(learning_rate,number_of_iter,alpha)
    model.fit_L2(x_tra, y_tra)
    Y_train_L2 = model.predict(x_tra)
    Y_test_L2=model.predict(x_tes)
    #print(sqrt(mean_squared_error(Y_train_p,y_train)),sqrt(mean_squared_error(Y_test_p,y_test)))
  
    reg_rmse_test_L2.append(RMSE(Y_test_L2,y_tes))
    reg_rmse_train_L2.append(RMSE(Y_train_L2,y_tra))
    iter_L2.append(number_of_iter)

print("L2 regularised test error: " ,reg_rmse_test_L2)
print("L2 regularised train error: ",reg_rmse_train_L2)

plt.plot(iter_L2,reg_rmse_test_L2)
plt.title("L2 Regularised_RMSE_Test")
plt.xlabel('Number of Iterartions')
plt.ylabel("RMSE")
plt.show()

plt.plot(iter_L2,reg_rmse_train_L2)
plt.xlabel('Number of Iterartions')
plt.ylabel("RMSE")
plt.title("L2 Regularised_RMSE_train")
plt.show()

plt.plot(iter_L2,reg_rmse_test_L2,label="Regularised Test RMSE")
plt.plot(iter_L2,reg_rmse_train_L2,label="Regularised Train RMSE")
plt.xlabel('Number of Iterartions')
plt.ylabel("RMSE")
plt.title("Combined Plot of L2 Regularised Test and Train RMSE")
plt.legend()
plt.show()

"""L1 regulaisation Hyper parameter tunning"""

lasso=Lasso()
lasso_regressor=GridSearchCV(lasso,param,scoring="neg_root_mean_squared_error", cv=5)
lasso_regressor.fit(x_tra,y_tra)

alp=lasso_regressor.best_params_['alpha']
print("Best hyperparameter for L1 case is:",alp)

"""Prediction using L1 regularised Linear model"""
iter_L1=[]
reg_L1_rmse_test=[]
reg_L1_rmse_train=[]


for number_of_iter in range(0,3000,300):
    model=Regularised_LinearRegression(learning_rate,number_of_iter,alp)
    model.fit_L1(x_tra, y_tra)
    Y_train_L1 = model.predict(x_tra)
    Y_test_L1=model.predict(x_tes)
    #print(sqrt(mean_squared_error(Y_train_p,y_train)),sqrt(mean_squared_error(Y_test_p,y_test)))
  
    reg_L1_rmse_test.append(RMSE(Y_test_L1,y_tes))
    reg_L1_rmse_train.append(RMSE(Y_train_L1,y_tra))
    iter_L1.append(number_of_iter)

print("L1 regularised test error: " ,reg_L1_rmse_test)
print("L1 regularised train error: " ,reg_L1_rmse_train)

plt.plot(iter_L1,reg_L1_rmse_test)
plt.title("L1_Regularised_RMSE_Test")
plt.xlabel('Number of Iterartions')
plt.ylabel("RMSE")
plt.show()

plt.plot(iter_L1,reg_L1_rmse_train)
plt.xlabel('Number of Iterartions')
plt.ylabel("RMSE")
plt.title("L1_Regularised_RMSE_train")
plt.show()

plt.plot(iter_L1,reg_L1_rmse_test,label="L1 Regularised Test RMSE")
plt.plot(iter_L1,reg_L1_rmse_train,label="L1 Regularised Train RMSE")
plt.xlabel('Number of Iterartions')
plt.ylabel("RMSE")
plt.title("Combined Plot of L1 Regularised Test and Train RMSE")
plt.legend()
plt.show()

"""part C """

dataset=pd.read_csv('/content/drive/MyDrive/data.csv')
dataset["W0"]=1

output=dataset['Body_Weight']
input=dataset.drop(['Body_Weight'],axis=1)
input.head()

model=LinearRegression(0.0001,1000)  
model.fit(input,output)
output_pre= model.predict(input)

plt.scatter(dataset['Brain_Weight'],dataset['Body_Weight'],c="blue")
plt.plot(dataset['Brain_Weight'],output_pre,c="red")
plt.title("Plot of Given Pts and Fitted Line with Linear model without Regularisation")
plt.xlabel("x -->")
plt.ylabel("y -->")

plt.show()

ridge=Ridge()
param={'alpha':[1e-10,1e-5,1e-3,1e-2,1e-1,0.3,0.8,1,10,100,1000]}
ridge_regressor=GridSearchCV(ridge,param,scoring="neg_root_mean_squared_error", cv=5)
ridge_regressor.fit(input,output)

alpha=ridge_regressor.best_params_['alpha']
print("Best hyperparameter for L2 case is:",alpha)

model_l2=Regularised_LinearRegression(0.0001,100,alpha)
model_l2.fit_L2(input,output)
out_pre_l2=model_l2.predict(input)

plt.scatter(dataset['Brain_Weight'],dataset['Body_Weight'],c="blue")
plt.plot(dataset['Brain_Weight'],out_pre_l2,c="red")
plt.title("Plot of Given Pts and Fitted Line with Linear model with L2 Regularisation")
plt.xlabel("x -->")
plt.ylabel("y -->")

plt.show()

lasso=Lasso()
lasso_regressor=GridSearchCV(lasso,param,scoring="neg_root_mean_squared_error", cv=5)
lasso_regressor.fit(input,output)

alp=lasso_regressor.best_params_['alpha']
print("Best hyperparameter for L1 case is:",alp)

model_l1=Regularised_LinearRegression(0.0001,100,alp)
model_l1.fit_L1(input,output)
out_pre_l1=model_l1.predict(input)

plt.scatter(dataset['Brain_Weight'],dataset['Body_Weight'],c="blue")
plt.plot(dataset['Brain_Weight'],out_pre_l1,c="red")
plt.title("Plot of Given Pts and Fitted Line with Linear model with L1 Regularisation")
plt.xlabel("x -->")
plt.ylabel("y -->")

plt.show()