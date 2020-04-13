import re
from io import StringIO
import json
from datetime import datetime, timedelta
import requests
import pandas as pd


class yahoo_data:
    """
    Retrieve the stock data from yahoo finance
    """
    timeout = 2
    crumb_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
    crumb_regex = r'CrumbStore":{"crumb":"(.*?)"}'
    yahoo_link = 'https://query1.finance.yahoo.com/v7/finance/download/{quote}?period1={dfrom}&period2={dto}&interval=1mo&events=history&crumb={crumb}'

    # initalizing construct to get the session
    def __init__(self, symbol):
        self.symbol = str(symbol)
        self.session = requests.session()

    def get_session(self):
        response = self.session.get(self.crumb_link.format(self.symbol), timeout=self.timeout)
        response.raise_for_status()
        match = re.search(self.crumb_regex, response.text)
        if not match:
            raise ValueError('could not find the session and crumb')
        else:
            self.crumb = match.group(1)

    def get_yahoo_quote(self):

        self.get_session()
        now = datetime.utcnow()
        date_to = int(now.timestamp())
        # timestamp format for date 3 January 1950
        date_from = -630961200
        url = self.yahoo_link.format(quote=self.symbol, dfrom=date_from, dto=date_to, crumb=self.crumb)
        response = self.session.get(url)
        response.raise_for_status()
        yahoo_df = pd.read_csv(StringIO(response.text), parse_dates=['Date'])
        return yahoo_df


class Response:
    """
    Response from the yahoo and fred API data
    """
    url = 'https://api.stlouisfed.org/fred/series/observations'

    def __init__(self):
        self.dates = []
        self.values = []

    def fred_response(self, params):
        """
        response data for fred_API
        :param params:
        :return:
        """
        params = dict(params)
        fred_response = requests.get(url=self.url, params=params)
        fred_json_res = json.loads(fred_response.text)['observations']
        for observation in fred_json_res:
            self.dates.append(str(observation['date']))
            self.values.append(float(observation['value']))

    def yahoo_response(self, id):
        id = str(id)
        # reverse the dataset
        yahoo_df = yahoo_data(id).get_yahoo_quote()[::-1]
        # reseting the dataframe index
        yahoo_df.reset_index(inplace=True)
        yahoo_df.drop('index', axis=1, inplace=True)
        # checking the most recent date
        most_recent_day = datetime.strptime(str(yahoo_df['Date'][0])[:10],
                                            '%Y-%m-%d').day
        if most_recent_day != 1:
            yahoo_df = yahoo_df[1:]
            yahoo_df.reset_index(inplace=True)
            yahoo_df.drop('index', axis=1, inplace=True)
        # extracting all dates in the dataframe adding these into the dates
        self.dates.extend([str(yahoo_df['Date'][index])[:10]
                           for index in range(0, len(yahoo_df))])
        # extracting all Adj close in yahoo finance
        self.values.extend([float(yahoo_df['Adj Close'][index])
                            for index in range(0, len(yahoo_df))])


class Dataset:
    """
    Contains the series id to fetch data from yahoo finance and fred API
    """
    api_key = 'f8e0e7a07dd220164976147cee128f16'
    def __init__(self):
        self.fred_series_ids = {'Non-farm_Payrolls': 'PAYEMS',
                                'Civilian_Unemployment_Rate': 'UNRATE',
                                'Effective_Fed_Funds': 'FEDFUNDS',
                                'CPI_All_Items': 'CPIAUCSL',
                                '10Y_Treasury_Rate': 'GS10',
                                '5Y_Treasury_Rate': 'GS5',
                                '3_Month_T-Bill_Rate': 'TB3MS',
                                'IPI': 'INDPRO',
                                'House_price_index':'CSUSHPISA'}
        self.yahoo_series_ids = {'S&P_500_Index': '^GSPC'}
        self.primary_output = {}

    def get_yahoo_data(self):
        import time
        for series_name in self.yahoo_series_ids.keys():
            res = Response()

            id = self.yahoo_series_ids[series_name]
            print(f"geting data for {series_name} {id}")
            try:
                res.yahoo_response(id)
            except requests.HTTPError:
                delay = 5
                print('\t --CONNECTION ERROR--',
                      '\n\t Sleeping for {} seconds.'.format(delay))
                time.sleep(delay)

            self.primary_output[series_name] = res
        print('Finished getting data from Yahoo Finance!')
        return self.primary_output

    def get_fred_data(self):
        import time
        now = datetime.now()
        month = now.strftime('%m')
        year = now.year
        most_recent_date = f'{year}-{month}-01'
        print('\nGetting data from FRED API as of {}...'.format(most_recent_date))
        for series_name in self.fred_series_ids.keys():
            res = Response()

            id = self.fred_series_ids[series_name]
            params = {'series_id': id,
                      'api_key': self.api_key,
                      'file_type': 'json',
                      'sort_order': 'desc',
                      'realtime_start': most_recent_date,
                      'realtime_end': most_recent_date}
            print(f"geting data for {series_name} {id}")
            try:
                res.fred_response(params)
            except requests.HTTPError:
                delay = 5
                print('\t --CONNECTION ERROR--',
                      '\n\t Sleeping for {} seconds.'.format(delay))
                time.sleep(delay)

            self.primary_output[series_name] = res
        return self.primary_output

