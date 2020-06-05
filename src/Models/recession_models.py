from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn import svm
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import xgboost as xgb
import pickle
import os
import numpy as np


class recession_models:

    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.features = ['Date', 'Payrolls_3mo_vs_12mo', 'Effective_Fed_Funds_12_chg', 'CPI_All_Items_3_mo_annualised',
                         '10Y_Treasury_Rate_12_chg', '3M_10Y_Treasury_Spread', 'S&P_500_Index_12_chg',
                         'Recession_in_6mo',
                         'Recession_in_12mo', 'Recession_in_24mo']
        self.df = pd.read_csv("Data/final_features.csv")[::-1]
        self.df = self.df[self.df['Date'] >= '1969-04-01']
        self.recession_data = self.df[self.features]
        self.file = ['Recession_in_6mo', 'Recession_in_12mo', 'Recession_in_24mo']
        self.recession = {'Date': self.recession_data['Date'].tolist()}
        self.price={}


    def models(self, id):
        for i in self.file:
            path = f'{self.path}/{i}.{id}'
            svmc = pickle.load(open(path, 'rb'))
            self.recession[i + '_probability'] = svmc.predict_proba(self.recession_data.iloc[:, 1:7])[:, 1].tolist()
        return self.recession

    def house_price(self, market,sports_facility,population,school,hospital,distance,room):
        for i in self.file:
            path = f'{self.path}/melbourne_house_price.rf'
            svmc = pickle.load(open(path, 'rb'))
            house_price = pd.DataFrame({'bedroom_count':[room] , 'Population':[population] , 'Distance from CBD': [distance], 'Hospital':[hospital] , 'School':[school] , 'Super Market':[market],'sports':[sports_facility]},dtype='int32')
            svmc.predict(house_price)
            self.price['melbourne_price']=np.round(svmc.predict(house_price).tolist(),2).tolist()

        return self.price

    def sydney_house(self, market,population,school,hospital,distance,room):
        for i in self.file:
            path = f'{self.path}/sydney_house_price.rf'
            svmc = pickle.load(open(path, 'rb'))
            house_price = pd.DataFrame({'bedroom_count':[room] , 'Population':[population] , 'Distance from CBD': [distance], 'Hospital':[hospital] , 'School':[school] , 'Super Market':[market]},dtype='int32')
            svmc.predict(house_price)
            self.price['sydney_price']=np.round(svmc.predict(house_price).tolist(),2).tolist()

        return self.price
