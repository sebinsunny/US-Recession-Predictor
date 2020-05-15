
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn import metrics
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split


# In[7]:


url = "E:/Company and NGO/Recession/companyandngo/Data/final_features.csv"
US_Dataset = pd.read_csv(url)
US_Dataset.head()


# In[8]:


#declaring variables for features
#le = preprocessing.LabelEncoder()
#Treasury_spread=le.fit_transform(US_Dataset['10Y_Treasury_Rate'])
#Unemployment_rate =le.fit_transform(US_Dataset['Civilian_Unemployment_Rate'])
#Recession_12months =le.fit_transform(US_Dataset['Recession_in_12mo'])
Treasury_spread = US_Dataset['3M_10Y_Treasury_Spread']
Treasury_rate_12months = US_Dataset['10Y_Treasury_Rate_12_chg']
#Unemployment_rate = US_Dataset['Civilian_Unemployment_Rate']
Payroll = US_Dataset['Payrolls_3mo_vs_12mo']
Sp_500_12months = US_Dataset['S&P_500_Index_12_month_pchg']
Effective_funds_12months = US_Dataset['Effective_Fed_Funds_12_chg']
Recession_6months = US_Dataset['Recession_in_6mo']
Recession_12months = US_Dataset['Recession_in_12mo']
Recession_24months = US_Dataset['Recession_in_24mo']


# In[9]:


#built gaussian classifies
Model_gb = GaussianNB()
Features = np.array(list(zip(Treasury_spread,Payroll,Sp_500_12months,Effective_funds_12months,Treasury_rate_12months)))
print(Features.shape)
#Predicting_variable = np.array(list(zip(Recession_6months,Recession_12months,Recession_24months)))
#print(Predicting_variable.shape)
#Model_gb.fit(Features,Recession_12months)


# In[10]:


#np.array.reshape(1, -1)
#lb = preprocessing.MultiLabelBinarizer()


X_train, X_test, y_train, y_test = train_test_split(Features,Recession_6months, test_size=0.30,random_state=350)
Model_gb.fit(X_train, y_train)
Prediction_for_6months = Model_gb.predict(X_test)
Prediction_for_6months


# In[12]:


#Evaluationg Model
print("Accuracy:",metrics.accuracy_score(y_test, Prediction_for_6months))


# In[13]:


#prediction for recession 12 months
X_train, X_test, y_train, y_test = train_test_split(Features,Recession_12months, test_size=0.30,random_state=350)
Model_gb.fit(X_train, y_train)
Prediction_for_12months= Model_gb.predict(X_test)
Prediction_for_12months
#Evaluationg Model
print("Accuracy:",metrics.accuracy_score(y_test, Prediction_for_12months))


# In[14]:


#prediction for recession 2 years
X_train, X_test, y_train, y_test = train_test_split(Features,Recession_24months, test_size=0.30,random_state=350)
Model_gb.fit(X_train, y_train)
Prediction_for_24months= Model_gb.predict(X_test)
Prediction_for_24months
#Evaluationg Model
print("Accuracy:",metrics.accuracy_score(y_test, Prediction_for_24months))

