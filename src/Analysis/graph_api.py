import re
from io import StringIO
import src.Data.retrieve_data as yh
import src.Data.retrieve_data as sk
import json
from datetime import datetime, timedelta
import requests
import pandas as pd


class feature_graph:
    api_key = 'f8e0e7a07dd220164976147cee128f16'
    common_dates = []
    url = 'https://api.stlouisfed.org/fred/series/observations'

    # https://api.stlouisfed.org/fred/series/observations?api_key=f8e0e7a07dd220164976147cee128f16&series_id=T10Y3M&sort_order=desc&frequency=m
    def __init__(self):
        self.fred_series_ids = {'Payroll': 'PAYEMS',
                                'Unemployment_Rate': 'UNRATE',
                                'Fed_Funds': 'FEDFUNDS',
                                'Consumer_Price_Index': 'CPIAUCSL',
                                '10Y_Treasury_Rate': 'GS10',
                                '5Y_Treasury_Rate': 'GS5',
                                '3_Month_Bill_Rate': 'TB3MS',
                                'spread': 'T10Y3M',
                                'IPI': 'INDPRO',
                                'House_price_index': 'CSUSHPISA',
                                'Recession': 'AUSRECD',
                                'yahoo': '^GSPC',
                                'twoyear': 'T10Y2Y',
                                'new':'key'}
        self.primary_output = {}

    def graph_api_data(self, name):
        if (name == 'yahoo'):
            data = sk.Dataset().get_yahoo_data()
            date = list(map(lambda x: x.strftime('%Y-%m-%d'), data['S&P_500_Index'].dates))
            self.primary_output['yahoo'] = [date, data['S&P_500_Index'].values]
            return self.primary_output
        else:
            import time
            now = datetime.now()
            month = int(now.strftime('%m'))
            year = now.year
            day = now.day
            most_recent_date = f'{year}-0{month}-{day}'
            print('\nGetting data from FRED API as of {}...'.format(most_recent_date))
            id = self.fred_series_ids[name]
            params = {'series_id': id,
                      'api_key': self.api_key,
                      'file_type': 'json',
                      'sort_order': 'desc',
                      'frequency': 'm'}
            print(f"geting data for {name}")
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
