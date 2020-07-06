#!/usr/bin/env python
# coding: utf-8

# In[3]:


#Creates animated race bar chart for comparing categories
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML


# In[28]:


#Read S&p 500 annual data, converting s&p value to float
df = pd.read_csv('C:/Users/chack/PycharmProjects/racinggraph/linetest.csv',thousands=',')
df["value"] = df.value.astype(float)


# In[68]:


fig, ax = plt.subplots(figsize=(15, 1))
#Function draw_barchart to plot bar chart for S&P500 for a year passed to it
def draw_barchart(year):
    dff = df[df['year'].eq(year)]
    ax.clear()    
    
    if(dff.eval(dff['value'] > 1200.00)):
        color1 = '#90d595'
    else:
        color1 ='#e48381'
     
    ax.barh(dff['name'], dff['value'],color= color1)
    plt.xlim(20,2800)
    dx = dff['value'].max() / 200

    for i, (value, name) in enumerate(zip(dff['value'], dff['name'])):
        ax.text(value-dx, i,     name,           size=14, weight=600, ha='right', va='bottom')
        ax.text(value+dx, i,     f'{value:,.0f}',  size=14, ha='left',  va='center')
        ax.text(1, 1, year, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    plt.box(False)
    plt.axis('off')
draw_barchart(2009)


# In[69]:


#Create animation for bar chart 
import matplotlib.animation as animation
from IPython.display import HTML
fig, ax = plt.subplots(figsize=(15, 1))
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(1968, 2019))
HTML(animator.to_jshtml()) 


# In[ ]:




