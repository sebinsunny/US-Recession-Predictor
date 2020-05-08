import re
from io import StringIO
import json
from datetime import datetime, timedelta
import requests
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt


class feature_graph:
    api_key = 'f8e0e7a07dd220164976147cee128f16'
    common_dates = []
    url = 'https://api.stlouisfed.org/fred/series/observations'

    def __init__(self):
        self.fred_series_ids = {'Payroll': 'PAYEMS',
                                'Unemployment_Rate': 'UNRATE',
                                'Fed_Funds': 'FEDFUNDS',
                                'Consumer_Price_Index': 'CPIAUCSL',
                                '10Y_Treasury_Rate': 'GS10',
                                '5Y_Treasury_Rate': 'GS5',
                                '3_Month_Bill_Rate': 'TB3MS',
                                'IPI': 'INDPRO',
                                'House_price_index': 'CSUSHPISA'}
        self.yahoo_series_ids = {'S&P_500': '^GSPC'}

        self.primary_output = {}

    def graph_api_data(self, name):
        import time
        now = datetime.now()
        month = int(now.strftime('%m'))
        year = now.year
        day = now.day - 1
        most_recent_date = f'{year}-0{month}-{day}'
        print('\nGetting data from FRED API as of {}...'.format(most_recent_date))
        id = self.fred_series_ids[name]
        params = {'series_id': id,
                  'api_key': self.api_key,
                  'file_type': 'json',
                  'sort_order': 'desc',
                  'realtime_start': most_recent_date,
                  'realtime_end': most_recent_date}
        print(f"geting data for name")
        try:
            fred_response = requests.get(url=self.url, params=params)
            dates = []
            values = []
            fred_json_res = json.loads(fred_response.text)['observations']
            if (params['series_id'] == 'CSUSHPISA' or 'CPIAUCSL'):
                for observation in fred_json_res:
                    if (observation['value'] != '.'):
                        dates.append(str(observation['date']))
                        values.append(float(observation['value']))


            else:
                for observation in fred_json_res:
                    dates.append(str(observation['date']))
                    values.append(float(observation['value']))
        except requests.HTTPError:
            delay = 5
            print('\t --CONNECTION ERROR--',
                  '\n\t Sleeping for {} seconds.'.format(delay))
            time.sleep(delay)
        self.primary_output[name] = [dates, values]
        print("success")
        return self.primary_output

#Class for data visualisation
class field_scatterplot:
    from scipy.misc import imsave
    df = pd.read_csv("Data/final_features.csv")
    g= scatter_matrix(df,figsize=(50,50))
    plt.savefig(r"figure_1.png")
