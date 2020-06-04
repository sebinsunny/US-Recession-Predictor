#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV


# In[31]:


# loading the cleaned and finalized dataset for US Recession Prediction
df_us =pd.read_csv('final_features.csv', skiprows=range(1, 13))#taking data until 12 months back of our latest date
df_us


# In[58]:


#setting up our input and output
X = df_us[["Civilian_Unemployment_Rate",'Payrolls_3mo_vs_12mo', 'Effective_Fed_Funds_12_chg', 'CPI_All_Items_3_mo_annualised',
            '10Y_Treasury_Rate_12_chg', 'S&P_500_Index_12_chg']]
Y = df_us["Recession_in_12mo"]
# train, test split on variables we are considering for recession prediction
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# In[59]:


#fitting a logistic regression model on our train dataset
lrm = sm.Logit(Y_train,X_train)
lr = lrm.fit()
#printing the summary of our model
print(lr.summary())


# In[60]:


#fitting a regularized logistic regression on train datsaet to reduce effects of multicollinearity and ofcourse overfitting.
LR = LogisticRegression(penalty='l2')
LR.fit(X_train,Y_train)
LR_pred = cross_val_predict(LR,X_train,Y_train,cv=5 )


# In[61]:


#confusion matrix will show our correct and incorrect predictions
confusion_matrix(Y_train,LR_pred)


# In[62]:


# checking the model accuracy
print("Model Accuracy :", LR.score(X_train, Y_train))


# In[63]:


#Logistic Regression ROC curve
LR_rocauc = ROCAUC(LR,size=(1080,720))
LR_rocauc.score(X_train, Y_train)
LR_r=LR_rocauc.poof()


# In[64]:


predicted_probs = pd.DataFrame(LR.predict_proba(X_test)[:,1])
predicted_probs.columns = ['Recession probability in 12 months']
predicted_probs


# In[65]:


predicted_probs.to_csv('F:\companyandngo\Prediction models\Logistic Regression Model/lr_model_12mo.csv',index=False)


# In[66]:


import pickle
pickle.dump(LR, open('F:\companyandngo\Prediction models\Logistic Regression Model/Recession_in_12mo.lr', 'wb'))


# In[67]:


#Fine Tuning

# implementing a Logistic Regression model with random hyperparameters
LR = LogisticRegression(penalty='l1',dual=False,max_iter=110, solver='liblinear')
LR.fit(X_train,Y_train)
LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, max_iter=110, multi_class='ovr', n_jobs=1,
          penalty='l1', random_state=None, solver='liblinear', tol=0.0001,
          verbose=0, warm_start=False)


# In[68]:


#setting the parameters
dual=[True,False]
max_iter=[100,110,120,130,140]
C = [1.0,1.5,2.0,2.5]
param_grid = dict(dual=dual,max_iter=max_iter,C=C)


# In[69]:


#implementing a Grid search on our defined hyperparameters
LR = LogisticRegression(penalty='l2')
G_search = GridSearchCV(estimator=LR, param_grid=param_grid, cv = 3, n_jobs=-1)
import time

starting_time = time.time()
G_search_results = G_search.fit(X_train,Y_train)
# Summarizing the  results
print("Best accuracy: %f gained by using this set of parameters%s" % (G_search_results.best_score_, G_search_results.best_params_))
print("time of execution: " + str((time.time() - starting_time)) + ' ms')


# In[70]:


#implementing a Random search on our defined hyperparameters
R_search = RandomizedSearchCV(estimator=LR, param_distributions=param_grid, cv = 3, n_jobs=-1)
starting_time = time.time()
R_search_results = R_search.fit(X_train,Y_train)
# Summarizing the  results
print("Best accuracy: %f gained by using this set of parameters%s" % (R_search_results.best_score_, R_search_results.best_params_))
print("time of execution: " + str((time.time() - starting_time)) + ' ms')

