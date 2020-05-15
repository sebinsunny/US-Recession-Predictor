#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import sklearn.metrics as metric
from sklearn import preprocessing
import math
from sklearn.metrics import accuracy_score
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


url = 'C:/Users/Rohit/Desktop/Deakin Assignments/Trimester 2 - March/Team Project Management - A/Project/companyandngo/Data/Datasets/AU Final.csv'
au_dataset = pd.read_csv(url)
au_dataset.head()


# In[4]:


au_dataset


# In[6]:


x = au_dataset['AORD_monthly_adj_closed']
y = au_dataset['Unemployment_Rate']
z = au_dataset['3M_10Y_Treasury_Spread']


# In[8]:


print("\n",x,"\n",y,"\n",z)


# In[9]:


data1 = np.array(list(zip(x,y,z)))
data1


# In[10]:


#6Month Recession

recession_6m = au_dataset['Recession_within_6M']
recession_6m


# In[11]:


#SVM For 6Month Recession

svc = svm.SVC(kernel='linear').fit(data1, recession_6m)
svc


# In[12]:


#Predicted Value for 6Month

y1_pred=svc.predict(data1)
y1_pred


# In[13]:


y1_true = recession_6m
y1_true


# In[15]:


#Confusion Matrix for 6Month Recession

confusion_matrix=metric.confusion_matrix(y1_true, y1_pred)
confusion_matrix

print("Confusion Matrix: \n", confusion_matrix)


# In[16]:


#Accuracy for 6Month Recession

accuracy_score(y1_true, y1_pred)


# In[19]:


#Perfomance Report for 6Month Recession
from sklearn.metrics import classification_report

print("Classification Report: \n", classification_report(y1_pred, y1_true))


# In[21]:


#12Month Recession

recession_12m = au_dataset['Recession_within_12M']
recession_12m


# In[32]:


#SVM For 12Month Recession

svc12 = svm.SVC(kernel='linear').fit(data1, recession_12m)
svc12


# In[33]:


#Predicted Value for 12Month

y2_pred=svc.predict(data1)
y2_pred


# In[34]:


y2_true = recession_12m
y2_true


# In[35]:


#Confusion Matrix for 12Month Recession

confusion_matrix_12=metric.confusion_matrix(y2_true, y2_pred)
confusion_matrix_12

print("Confusion Matrix: \n", confusion_matrix_12)


# In[36]:


#Accuracy for 12Month Recession

accuracy_score(y2_true, y2_pred)


# In[37]:


#Perfomance Report for 12Month Recession
from sklearn.metrics import classification_report

print("Classification Report: \n", classification_report(y2_pred, y2_true))


# In[38]:


#24Month Recession

recession_24m = au_dataset['Recession_within_24M']
recession_24m


# In[31]:


#SVM For 24Month Recession

svc24 = svm.SVC(kernel='linear').fit(data1, recession_24m)
svc24


# In[39]:


#Predicted Value for 24Month

y3_pred=svc.predict(data1)
y3_pred


# In[41]:


y3_true = recession_24m
y3_true


# In[43]:


#Confusion Matrix for 24Month Recession

confusion_matrix_24=metric.confusion_matrix(y3_true, y3_pred)
confusion_matrix_24

print("Confusion Matrix: \n", confusion_matrix_24)


# In[44]:


#Accuracy for 24Month Recession

accuracy_score(y3_true, y3_pred)


# In[45]:


#Perfomance Report for 24Month Recession
from sklearn.metrics import classification_report

print("Classification Report: \n", classification_report(y3_pred, y3_true))


# In[ ]:





# In[ ]:





# In[ ]:




