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


class recession_models:

    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.features = ['Date', 'Payrolls_3mo_vs_12mo', 'Effective_Fed_Funds_12_chg', 'CPI_All_Items_3_mo_annualised',
                         '10Y_Treasury_Rate_12_chg', '3M_10Y_Treasury_Spread', 'S&P_500_Index_12_chg',
                         'Recession_in_6mo',
                         'Recession_in_12mo', 'Recession_in_24mo']
        self.df = pd.read_csv("Data/final_features.csv")[::-1]
        self.recession_data = self.df[self.features]
        self.file = ['Recession_in_6mo', 'Recession_in_12mo', 'Recession_in_24mo']
        self.recession = {'Date': self.recession_data['Date'].tolist()}

    def models(self, id):
        for i in self.file:
            svmc = pickle.load(open(self.path + '/' + i + '.' + id, 'rb'))
            self.recession[i + '_probability'] = svmc.predict_proba(self.recession_data.iloc[:, 1:7])[:, 1].tolist()
        return self.recession
