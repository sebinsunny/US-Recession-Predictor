#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import numpy as np


# In[2]:


#read final feature file and select required columns
df= pd.read_csv("C:/Users/chack/Documents/companyandngo2/Data/final_features.csv")
df_model = df[['Date', 'Payrolls_3mo_vs_12mo', 'Effective_Fed_Funds_12_chg', 'CPI_All_Items_3_mo_annualised',
            '10Y_Treasury_Rate_12_chg', '3M_10Y_Treasury_Spread', 'S&P_500_Index_12_chg','Recession_in_6mo','Recession_in_12mo','Recession_in_24mo']]

#copy records prior 2018-05-20 to be used for model training
df_model_prior18 = df_model[df_model['Date'] < '2018-05-20']
df_model_post18 = df_model[df_model['Date'] > '2018-05-20']
df_model_post18_nodate = df_model_post18.iloc[:,1:7]
dates = df_model_post18['Date']


# In[3]:


#Function to split test and train data for 6 and 12 month recession
def testdata_traindata_split(col_no):
    from sklearn.model_selection import train_test_split
    X,y = df_model_prior18.iloc[:,1:-3],df_model_prior18.iloc[:,col_no]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    return(X_train, X_test, y_train, y_test)


# In[4]:


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
         param_grid = param_test1, scoring='recall',n_jobs=4,iid=False, cv=5)
    gsearch4.fit(X_train,y_train)

    print("Grid scores on development set:")
    means = gsearch4.cv_results_['mean_test_score']
    stds = gsearch4.cv_results_['std_test_score']
#     for mean, std, params in zip(means, stds, gsearch4.cv_results_['params']):
#         print("%0.3f (+/-%0.03f) for %r"
#         % (mean, std * 2, params))
    print(f'Best score for {month} month recession :{gsearch4.best_score_}')
    print(f'Params for {month} month recession :{gsearch4.best_params_}')
    max_depth = gsearch4.best_params_['max_depth']
    colsample_bytree = gsearch4.best_params_['colsample_bytree']
    gamma = gsearch4.best_params_['gamma']
    reg_alpha = gsearch4.best_params_['reg_alpha']
    return(max_depth,colsample_bytree,gamma,reg_alpha)


# In[5]:


#Create test and trianing data for 6 and 12 months
X_train, X_test, y_train_6mo, y_test_6mo = testdata_traindata_split(7)
X_train, X_test, y_train_12mo, y_test_12mo = testdata_traindata_split(8)
X_train, X_test, y_train_24mo, y_test_24mo = testdata_traindata_split(9)


# In[6]:


#Print best xgb paramters for 6 month modelling
max_depth6,colsample_bytree6,gamma6,reg_alpha6 = best_parmeter_xgb(X_train,y_train_6mo,'6')
max_depth12,colsample_bytree12,gamma12,reg_alpha12 = best_parmeter_xgb(X_train,y_train_12mo,'12')
max_depth24,colsample_bytree24,gamma24,reg_alpha24 = best_parmeter_xgb(X_train,y_train_24mo,'24')


# In[7]:


#Build and train 6 month and 12 month xgb model
best_model_6mo = xgb.XGBClassifier(objective ='binary:logistic', learning_rate = 0.1,reg_lambda=0.01,colsample_bytree=colsample_bytree6,
                 gamma=gamma6,booster='gbtree',alpha = 10, n_estimators = 10,max_depth=max_depth6,reg_alpha=reg_alpha6)
best_model_12mo = xgb.XGBClassifier(objective ='binary:logistic', learning_rate = 0.1,reg_lambda=0.01,colsample_bytree=colsample_bytree12,
                 gamma=gamma12,booster='gbtree',alpha = 10, n_estimators = 10,max_depth=max_depth12,reg_alpha=reg_alpha12)
best_model_24mo = xgb.XGBClassifier(objective ='binary:logistic', learning_rate = 0.1,reg_lambda=0.01,colsample_bytree=colsample_bytree24,
                 gamma=gamma24,booster='gbtree',alpha = 10, n_estimators = 10,max_depth=max_depth24,reg_alpha=reg_alpha24)


best_model_6mo.fit(X_train,y_train_6mo)
best_model_12mo.fit(X_train,y_train_12mo)
best_model_24mo.fit(X_train,y_train_24mo)


# In[8]:


predicted_probs_6mo = pd.DataFrame(best_model_6mo.predict_proba(df_model_post18_nodate)[:,1])
predicted_probs_12mo = pd.DataFrame(best_model_12mo.predict_proba(df_model_post18_nodate)[:,1])
predicted_probs_24mo = pd.DataFrame(best_model_24mo.predict_proba(df_model_post18_nodate)[:,1])
recession_probabilities = pd.concat([dates,predicted_probs_6mo,predicted_probs_12mo,predicted_probs_24mo],axis =1)
recession_probabilities.columns = ['Date','Recession probability in 6 months','Recession probability in 12 months','Recession Probability in 24 months']
recession_probabilities


# In[9]:


recession_probabilities.to_csv('C:/Users/chack/Documents/companyandngo/XGB_model1_accuracy.csv',index=False)


# In[10]:


import pickle
pickle.dump(best_model_6mo, open('C:/Users/chack/Documents/companyandngo2/Recession_in_6mo.xg', 'wb'))
pickle.dump(best_model_12mo, open('C:/Users/chack/Documents/companyandngo2/Recession_in_12mo.xg', 'wb'))
pickle.dump(best_model_24mo, open('C:/Users/chack/Documents/companyandngo2/Recession_in_24mo.xg', 'wb'))


# In[ ]:





# In[ ]:




