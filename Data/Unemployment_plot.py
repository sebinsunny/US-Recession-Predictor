#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# setting up our figure size
plt.rcParams['figure.figsize']=(20,10) 
 # using a theme for better visualization
plt.style.use('fivethirtyeight')
# Read the AU Dataset
AU_Final = pd.read_csv('C:/Users/chack/Documents/companyandngo/Data/Datasets/AU Final.csv')


# In[5]:


AU_Final.Date = pd.to_datetime(AU_Final.Date) 
AU_Final.set_index('Date', inplace=True) 


# In[72]:


def draw_linechart(i):    
    ax1.clear()      
    ax2 = ax1.twinx()
    ax1.plot(AU_Final['Unemployment_Rate'][:i], color="purple")
    ax2.bar(AU_Final.index, AU_Final.Recession,width=20, alpha=0.4, color='red') #second axis
    ax2.grid(b=False)
    ax1.grid(b=False)
    ax1.set_title('Unemployment Rate Variation')
    ax1.set_ylabel('Unemployment Rate(%)')
    ax2.set_axis_off()
    ax1.set_ylim([2,12])
    plt.grid(b=None)


# In[73]:


import matplotlib.animation as animation
from IPython.display import HTML
fig, ax1 = plt.subplots(figsize=(20, 10))
animator = animation.FuncAnimation(fig, draw_linechart, frames=range(0,425,25))
HTML(animator.to_jshtml()) 


# In[ ]:




