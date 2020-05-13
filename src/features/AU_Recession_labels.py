#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


AU_Final = pd.read_csv("au final.csv")


# In[3]:


# Creating labels for recession in 6 months , 12 months and 24 months
def recession_6M_12M_24M():
     # creating columns for recession within 6moths, 12 months and 24 months
     row_no = len(AU_Final)
     AU_Final['Recession_within_6M'] = [0] * row_no
     AU_Final['Recession_within_12M'] = [0] * row_no
     AU_Final['Recession_within_24M'] = [0] * row_no

     # If recession label is 1, add 1 to Recession_within_6M,Recession_within_12M,Recession_within_24M

     for index in range(0, len(AU_Final)):
         if AU_Final['Recession'][index] == 1:
             AU_Final.loc[min(index + 6, len(AU_Final) - 1),'Recession_within_6M'] = 1
             AU_Final.loc[min(index + 12, len(AU_Final) - 1),'Recession_within_12M'] = 1
             AU_Final.loc[min(index + 24, len(AU_Final) - 1),'Recession_within_24M'] = 1


# In[4]:


recession_6M_12M_24M()


# In[5]:


AU_Final.to_csv("AU Final.csv",index=False)

