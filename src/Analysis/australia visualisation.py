#!/usr/bin/env python
# coding: utf-8

# In[13]:


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
AU_Final = pd.read_csv('C:/Users/chack/Documents/companyandngo2/Data/Datasets/AUFinal.csv')
AU_Final = AU_Final.iloc[::-1]
# AU_Final.sort_values(by=['Date'])


# In[14]:


AU_Final.Date = pd.to_datetime(AU_Final.Date) 
AU_Final.set_index('Date', inplace=True) 


# In[20]:


def draw_linechart_unemployment(i):    
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


# In[16]:


import matplotlib.animation as animation
from IPython.display import HTML
fig, ax1 = plt.subplots(figsize=(20, 10))
animator = animation.FuncAnimation(fig, draw_linechart, frames=range(0,425,100))
HTML(animator.to_jshtml()) 


# In[26]:


def draw_linechart_treasuryspread(i):    
    ax1.clear()      
    ax2 = ax1.twinx()
    ax1.plot(AU_Final['3M_10Y_Treasury_Spread'][:i], color="purple")
    ax2.bar(AU_Final.index, AU_Final.Recession,width=20, alpha=0.4, color='red') #second axis
    ax2.grid(b=False)
    ax1.grid(b=False)
    ax1.set_title('3M_10Y_Treasury_Spread')
    ax1.set_ylabel('3M_10Y_Treasury_Spread')
    ax2.set_axis_off()
    ax1.set_ylim([-7,7])
    plt.grid(b=None)


# In[27]:


def draw_linechart_AORD(i):    
    ax1.clear()      
    ax2 = ax1.twinx()
    ax1.plot(AU_Final['AORD_monthly_adj_closed'][:i], color="purple")
    ax2.bar(AU_Final.index, AU_Final.Recession,width=20, alpha=0.4, color='red') #second axis
    ax2.grid(b=False)
    ax1.grid(b=False)
    ax1.set_title('AORD_monthly_adj_closed')
    ax1.set_ylabel('AORD_monthly_adj_closed')
    ax2.set_axis_off()
    ax1.set_ylim([600,8000])
    plt.grid(b=None)


# In[21]:


#plot for unemployment
import matplotlib.animation as animation
from IPython.display import HTML
fig, ax1 = plt.subplots(figsize=(20, 10))
animator = animation.FuncAnimation(fig, draw_linechart_unemployment, frames=range(0,425,25))
HTML(animator.to_jshtml()) 


# In[28]:


#AORD plot
import matplotlib.animation as animation
from IPython.display import HTML
fig, ax1 = plt.subplots(figsize=(20, 10))
animator = animation.FuncAnimation(fig, draw_linechart_AORD, frames=range(0,425,25)
HTML(animator.to_jshtml()) 


# In[29]:


#Treasury spread plot
import matplotlib.animation as animation
from IPython.display import HTML
fig, ax1 = plt.subplots(figsize=(20, 10))
animator = animation.FuncAnimation(fig, draw_linechart_treasuryspread, frames=range(0,425,25))
HTML(animator.to_jshtml()) 


# In[ ]:




