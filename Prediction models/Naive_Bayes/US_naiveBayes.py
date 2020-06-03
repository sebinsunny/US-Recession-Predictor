#!/usr/bin/env python
# coding: utf-8

# In[311]:


import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn import metrics
import numpy as np
#from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc,precision_score, accuracy_score, recall_score, f1_score
import matplotlib.pyplot as plt
import pickle


# In[273]:


path = "C:/Users/61487/Desktop/CompanyNGO/companyandngo/Data/"
All_data = pd.read_csv(path + 'final_features.csv')
US_Dataset = pd.read_csv(path + 'final_features.csv',skiprows=range(1, 6))
US_Dataset.head()


# In[277]:


#declaring variables for features

#Treasury_spread=le.fit_transform(US_Dataset['10Y_Treasury_Rate'])
#Unemployment_rate =le.fit_transform(US_Dataset['Civilian_Unemployment_Rate'])
#Recession_12months =le.fit_transform(US_Dataset['Recession_in_12mo'])
#Treasury_spread = US_Dataset['3M_10Y_Treasury_Spread']
#Treasury_rate_12months = US_Dataset['10Y_Treasury_Rate_12_chg']
#Unemployment_rate = US_Dataset['Civilian_Unemployment_Rate']
#Payroll = US_Dataset['Payrolls_3mo_vs_12mo']
#Sp_500_12months = US_Dataset['S&P_500_Index_12_month_pchg']
#Effective_funds_12months = US_Dataset['Effective_Fed_Funds_12_chg']
Recession_6months = US_Dataset['Recession_in_6mo']

Recession_12months =  US_Dataset['Recession_in_12mo']

date = All_data['Date']
Recession_24months = US_Dataset['Recession_in_24mo']

#Date = US_Dataset['Date']
Features = ['Date', 'Payrolls_3mo_vs_12mo', 'Effective_Fed_Funds_12_chg', 'CPI_All_Items_3_mo_annualised',
            '10Y_Treasury_Rate_12_chg', '3M_10Y_Treasury_Spread', 'S&P_500_Index_12_chg','Recession_in_6mo','Recession_in_12mo','Recession_in_24mo']
recession_dataset  = US_Dataset[Features]


# In[260]:



#built gaussian classifies
Model_gb = GaussianNB()
#Features = np.array(list(zip(Treasury_spread,Payroll,Effective_funds_12months,Treasury_rate_12months)))

#Predicting_variable = np.array(list(zip(Recession_6months,Recession_12months,Recession_24months)))
#print(Predicting_variable.shape)
#Model_gb.fit(Features,Recession_12months)


# In[299]:



#np.array.reshape(1, -1)
#lb = preprocessing.MultiLabelBinarizer()

#predicting for 6months
X_train, X_test, y_train, y_test = train_test_split(recession_dataset.iloc[:,1:6],Recession_6months,test_size=0.3,random_state=10)
Model_gb.fit(X_train, y_train)
Prediction_for_6months = Model_gb.predict(X_test)
Prediction_for_6months 


# In[307]:



#Evaluationg Model
print("Accuracy:",metrics.accuracy_score(y_test, Prediction_for_6months))
recession_predicted_6 = pd.DataFrame(Model_gb.predict_proba(X_test)[:,1])
ROC_AUC=roc_auc_score(y_test,recession_predicted_6)
ROC_AUC
recession_predicted_6mo = pd.DataFrame(recession_predicted_6)
recession_predicted_6mo
recession_predicted_6mo.to_csv('C:/Users/61487/Desktop/CompanyNGO/companyandngo/Prediction models/Naive_Bayes/Naives_6mo.csv',index=False)


# In[309]:


#prediction for recession 12 months
X_train, X_test, y_train, y_test = train_test_split(recession_dataset.iloc[:,1:6],Recession_12months, test_size=0.30,random_state=350)
Model_gb.fit(X_train, y_train)
Prediction_for_12months= Model_gb.predict(X_test)
Prediction_for_12months
#Evaluationg Model
print("Accuracy:",metrics.accuracy_score(y_test, Prediction_for_12months))
recession_predicted_12 = pd.DataFrame(Model_gb.predict_proba(X_test)[:,1])
ROC_AUC=roc_auc_score(y_test,recession_predicted_12)
ROC_AUC
recession_predicted_12 = pd.DataFrame(recession_predicted_12)
recession_predicted_12
recession_predicted_12.to_csv('C:/Users/61487/Desktop/CompanyNGO/companyandngo/Prediction models/Naive_Bayes/Naives_12mo.csv',index=False)


# In[310]:



#prediction for recession 2 years
X_train, X_test, y_train, y_test = train_test_split(recession_dataset.iloc[:,1:5],Recession_24months, test_size=0.30,random_state=350)
Model_gb.fit(X_train, y_train)
Prediction_for_24months= Model_gb.predict(X_test)
print(Prediction_for_24months)
#Evaluationg Model
print("Accuracy:",metrics.accuracy_score(y_test, Prediction_for_24months))
recession_predicted_24 = pd.DataFrame(Model_gb.predict_proba(X_test)[:,1])
ROC_AUC=roc_auc_score(y_test,recession_predicted_24)
ROC_AUC

recession_predicted_24 
recession_predicted_24.to_csv('C:/Users/61487/Desktop/CompanyNGO/companyandngo/Prediction models/Naive_Bayes/Naives_24mo.csv',index=False)


# In[319]:



recession_probabilities = pd.concat([date,recession_predicted_6mo,recession_predicted_12,recession_predicted_24 ],axis =1)
recession_probabilities.columns = ['Date','Recession probability in 6 months','Recession probability in 12 months','Recession probability in 24 months']
recession_probabilities.head(20)
y_axis = ['Recession probability in 6 months','Recession probability in 12 months','Recession probability in 24 months']

recession_probabilities.plot('Date', y_axis,figsize =(20,4))


# In[312]:


pickle.dump(recession_predicted_6, open('C:/Users/61487/Desktop/CompanyNGO/companyandngo/Prediction models/Naive_Bayes/Recession_in_6mo.nb', 'wb'))
pickle.dump(recession_predicted_12, open('C:/Users/61487/Desktop/CompanyNGO/companyandngo/Prediction models/Naive_Bayes/Recession_in_12mo.nb', 'wb'))
pickle.dump(recession_predicted_24, open('C:/Users/61487/Desktop/CompanyNGO/companyandngo/Prediction models/Naive_Bayes/Recession_in_24mo.nb', 'wb'))

