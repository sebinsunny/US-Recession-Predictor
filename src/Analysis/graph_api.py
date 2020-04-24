import re
from io import StringIO
import json
from datetime import datetime, timedelta
import requests
import pandas as pd


class feature_graph:
    api_key = 'f8e0e7a07dd220164976147cee128f16'
    common_dates = []
    url = 'https://api.stlouisfed.org/fred/series/observations'

    def __init__(self):
        self.fred_series_ids = {'Non-farm_Payrolls': 'PAYEMS',
                                'Civilian_Unemployment_Rate': 'UNRATE',
                                'Effective_Fed_Funds': 'FEDFUNDS',
                                'CPI_All_Items': 'CPIAUCSL',
                                '10Y_Treasury_Rate': 'GS10',
                                '5Y_Treasury_Rate': 'GS5',
                                '3_Month_T-Bill_Rate': 'TB3MS',
                                'IPI': 'INDPRO',
                                'House_price_index': 'CSUSHPISA'}
        self.yahoo_series_ids = {'S&P_500_Index': '^GSPC'}

        self.primary_output = {}

    def graph_api_data(self):
        import time
        now = datetime.now()
        month = int(now.strftime('%m'))
        year = now.year
        day = now.day - 1
        most_recent_date = f'{year}-0{month}-{day}'
        print('\nGetting data from FRED API as of {}...'.format(most_recent_date))
        for series_name in self.fred_series_ids.keys():

            id = self.fred_series_ids[series_name]
            params = {'series_id': id,
                      'api_key': self.api_key,
                      'file_type': 'json',
                      'sort_order': 'desc',
                      'realtime_start': most_recent_date,
                      'realtime_end': most_recent_date}
            print(f"geting data for {series_name} {id}")
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
            self.primary_output[series_name] = [dates, values]

        print("kk")
        return self.primary_output
