#!/usr/bin/env python
# coding: utf-8

# In[136]:



#importing necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


Us_data = pd.read_csv('C:/Users/61487/Desktop/CompanyNGO/companyandngo/Data/final_features.csv')
#print(plt.style.available)

plt.style.use('seaborn-poster')
plt.rcParams['figure.figsize'] = (15, 10)



# In[137]:


Us_data.Date = pd.to_datetime(Us_data['Date'])
Us_data.set_index('Date', inplace = True)


# In[134]:



fig, axis1 = plt.subplots()
axis1.clear()
axis2 = axis1.twinx() 
axis1.plot(Us_data['3M_10Y_Treasury_Spread'])
axis2.bar(Us_data.index, Us_data.Recession,width=20, alpha=0.5, color='red')
axis1.grid(b=False)
axis2.grid(b=False) 
axis1.set_ylim([-3,9])
axis1.set_title("U.S. 3 months and 10 years treasury rate spread vs Recession",color='black')
axis1.set_ylabel('3 months and 10 years treasury rate spread',color='black')
plt.axis('off')


# In[ ]:





# In[ ]:




