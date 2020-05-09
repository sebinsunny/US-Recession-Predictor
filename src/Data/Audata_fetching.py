#!/usr/bin/env python
# coding: utf-8

# In[18]:


# importing the necessary libraries
import  requests
import json
import pandas as pd


# In[19]:


#fetching the data from API
dates=[]
values=[]
# giving the key for the feature and the api_key
r = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=AUSRECM&api_key=f8e0e7a07dd220164976147cee128f16&file_type=json&frequency=m')
r = json.loads(r.text)['observations']
for observations in r:
    if (observation['value'] != '.'):
        dates.append(str(observations['date']))
        values.append(float(observations['value']))
#storing the data into a dataframe 
df = pd.DataFrame()
df['Date']=dates
df['values']=values
#saving it as a csv file
df.to_csv("AUrecession_labels.csv", index=False)

