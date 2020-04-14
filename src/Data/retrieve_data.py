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
        if (params['series_id'] == 'CSUSHPISA'):
            for observation in fred_json_res:
                if (observation['value'] != '.'):
                    self.dates.append(datetime.strptime(str(observation['date']), '%Y-%m-%d'))
                    self.values.append(float(observation['value']))


        else:
            for observation in fred_json_res:
                self.dates.append(datetime.strptime(str(observation['date']), '%Y-%m-%d'))
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
    common_dates = []
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
        self.shortest_name_length = 1000000
        self.shortest_series_name = ''

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
        month = int(now.strftime('%m')) - 2
        year = now.year
        most_recent_date = '2020-04-13'  # f'{year}-0{month}-01'
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
        self.sort_data()
        print('Finished getting data from Fred API')

    def get_common_dates(self):
        for i in self.fred_series_ids:
            self.common_dates.append(self.primary_output[i].dates)

    def get_dates(self,seriesid):
        mindate=[]
        maxdate=[]
        for i in self.fred_series_ids:
            if i == seriesid:
                continue
            mindate.append(min(self.primary_output[i].dates))
            maxdate.append(max(self.primary_output[i].dates))

        self.start_date = max(mindate)
        self.end_date = min(maxdate)

    def fetch_data(self,startdate,enddate,seriesid):
        df = pd.DataFrame()
        for series_name in list(self.fred_series_ids):
            a = []
            k = 0
            if series_name == seriesid:
                continue
            for j in list(self.primary_output[series_name].dates):
                if ((j >= self.start_date) and (j <= self.end_date)):
                    a.append(self.primary_output[series_name].values[k])
                k = k + 1
            df[series_name]=a
        return df



    def sort_data(self):
        self.get_dates('House_price_index')
        df_house_price = self.fetch_data(self.start_date,self.end_date,"House_price_index")
        self.get_dates('allfields')
        df_all = self.fetch_data(self.start_date, self.end_date, "all")






