#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import numpy as np


# In[2]:


#read final feature file and select required columns
df= pd.read_csv("C:/Users/chack/Documents/companyandngo/Data/final_features.csv")
df_model = df[['Date', 'Payrolls_3mo_vs_12mo', 'Effective_Fed_Funds_12_chg', 'CPI_All_Items_3_mo_annualised',
            '10Y_Treasury_Rate_12_chg', '3M_10Y_Treasury_Spread', 'S&P_500_Index_12_chg','Recession_in_6mo','Recession_in_12mo','Recession_in_24mo']]
#copy records prior 2018-05-20 to be used for model training
df_model_prior18 = df_model[df_model['Date'] < '2018-05-20']
df_model_post18 = df_model[df_model['Date'] > '2018-05-20']
df_model_post18_nodate = df_model_post18.iloc[:,1:7]


# In[5]:


#Function to split test and train data for 6 and 12 month recession
def testdata_traindata_split(col_no):
    from sklearn.model_selection import train_test_split
    X,y = df_model_prior18.iloc[:,1:-3],df_model_prior18.iloc[:,col_no]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    return(X_train, X_test, y_train, y_test)


# In[20]:


#Function to use cross validation to determine best paramter for xgb
def best_parmeter_xgb(X_train,y_train,month):
    from sklearn.model_selection import GridSearchCV
    param_test1 = {
     'max_depth':range(3,10,1),
     'gamma':[i/10.0 for i in range(0,5)],
     'colsample_bytree':[i/10.0 for i in range(1,10)],
     'reg_alpha':[0, 0.001, 0.005, 0.01, 0.05]    
    }

    gsearch4 = GridSearchCV(estimator = xgb.XGBClassifier(objective ='binary:logistic', learning_rate = 0.1,reg_lambda=0.01,
                 booster='gbtree',alpha = 10, n_estimators = 10), 
         param_grid = param_test1, scoring='roc_auc',n_jobs=4,iid=False, cv=5)
    gsearch4.fit(X_train,y_train)

    print("Grid scores on development set:")
    means = gsearch4.cv_results_['mean_test_score']
    stds = gsearch4.cv_results_['std_test_score']
#     for mean, std, params in zip(means, stds, gsearch4.cv_results_['params']):
#         print("%0.3f (+/-%0.03f) for %r"
#         % (mean, std * 2, params))
    print(f'Best score for {month} month recession :{gsearch4.best_score_}')
    print(f'Params for {month} month recession :{gsearch4.best_params_}')


# In[14]:


#Create test and trianing data for 6 and 12 months
X_train, X_test, y_train_6mo, y_test_6mo = testdata_traindata_split(7)
X_train, X_test, y_train_12mo, y_test_12mo = testdata_traindata_split(8)


# In[21]:


#Print best xgb paramters for 6 month modelling
best_parmeter_xgb(X_train,y_train_6mo,'6')


# In[22]:


#Print best xgb paramters for 12 month modelling
best_parmeter_xgb(X_train,y_train_12mo,'12')


# In[23]:


#Build and train 6 month and 12 month xgb model
best_model_6mo = xgb.XGBClassifier(objective ='binary:logistic', learning_rate = 0.1,reg_lambda=0.01,colsample_bytree=0.9,
                 gamma=0.3,booster='gbtree',alpha = 10, n_estimators = 10,max_depth=5,reg_alpha=0)
best_model_12mo = xgb.XGBClassifier(objective ='binary:logistic', learning_rate = 0.1,reg_lambda=0.01,colsample_bytree=0.9,
                 gamma=0.0,booster='gbtree',alpha = 10, n_estimators = 10,max_depth=7,reg_alpha=0.05)

best_model_6mo.fit(X_train,y_train_6mo)
best_model_12mo.fit(X_train,y_train_12mo)


# In[27]:


df_model_post18_nodate = df_model_post18.iloc[:,1:7]
dates = df_model_post18['Date']
df_model_post18_nodate


# In[28]:


predicted_probs_6mo = pd.DataFrame(best_model_6mo.predict_proba(df_model_post18_nodate)[:,1])
predicted_probs_6mo


# In[29]:


predicted_probs_12mo = pd.DataFrame(best_model_12mo.predict_proba(df_model_post18_nodate)[:,1])
predicted_probs_12mo


# In[33]:


recession_probabilities = pd.concat([dates,predicted_probs_6mo,predicted_probs_12mo],axis =1)
recession_probabilities.columns = ['Date','Recession probability in 6 months','Recession probability in 12 months']
recession_probabilities


# In[37]:


recession_probabilities.to_csv('C:/Users/chack/Documents/companyandngo/XGB_model1.csv',index=False)


# In[40]:


import pickle
pickle.dump(best_model_6mo, open('C:/Users/chack/Documents/companyandngo/xgb_6mo.xg', 'wb'))
pickle.dump(best_model_12mo, open('C:/Users/chack/Documents/companyandngo/xgb_12mo.xg', 'wb'))


# In[ ]:




