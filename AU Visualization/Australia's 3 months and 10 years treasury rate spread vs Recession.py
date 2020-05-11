#!/usr/bin/env python
# coding: utf-8

# In[5]:


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
AU_Final = pd.read_csv('AU Final.csv') 
#setting date column to datetime
AU_Final.Date = pd.to_datetime(AU_Final.Date) 
#setting date column as index
AU_Final.set_index('Date', inplace=True) 

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # setting up the second axis
ax1.plot(AU_Final['3M_10Y_Treasury_Spread']) #first axis
ax2.bar(AU_Final.index, AU_Final.Recession,width=20, alpha=0.4, color='red') #second axis
ax2.grid(b=False) # turning off the grid line of the second axis for cleaner visualization
ax1.set_ylim([-6,6]) #setting up a limmit on first axis
#giving meaningful names to the chart and both axises 
ax1.set_title("Australia's 3 months and 10 years treasury rate spread vs Recession")
ax1.set_ylabel('3 months and 10 years treasury rate spread')
ax2.set_ylabel('Recession')

