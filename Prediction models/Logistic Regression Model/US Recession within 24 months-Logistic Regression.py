#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import statsmodels.api as sm
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
import sys
get_ipython().system('{sys.executable} -m pip install yellowbrick')
from yellowbrick.classifier import ROCAUC


# In[2]:


# loading the cleaned and finalized dataset for US Recession Prediction
df_us =pd.read_csv('final_features.csv')
df_us


# In[3]:


#setting up our input and output
X = df_us[["Civilian_Unemployment_Rate","3M_10Y_Treasury_Spread"]]
Y = df_us["Recession_in_24mo"]
# train, test split on variables we are considering for recession prediction
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# In[4]:


#fitting a logistic regression model on our train dataset
lrm = sm.Logit(Y_train,X_train)
lr = lrm.fit()
#printing the summary of our model
print(lr.summary())


# In[5]:


#fitting a regularized logistic regression on train datsaet to reduce effects of multicollinearity and ofcourse overfitting.
LR = LogisticRegression(penalty='l2')
LR.fit(X_train,Y_train)
LR_pred = cross_val_predict(LR,X_train,Y_train,cv=5 )


# In[6]:


#confusion matrix will show our correct and incorrect predictions
confusion_matrix(Y_train,LR_pred)


# In[9]:


# checking the model accuracy
print("Model Accuracy :", LR.score(X_train, Y_train))


# In[8]:


#Logistic Regression ROC curve
LR_rocauc = ROCAUC(LR,size=(1080,720))
LR_rocauc.score(X_train, Y_train)
LR_r=LR_rocauc.poof()

