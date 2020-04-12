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

    def __init__(self):
        self.dates = []
        self.values = []

    def fred_response(self, params):
        """
        response data for fred_API
        :param params:
        :return:
        """

    def yahoo_response(self, id):
        id = str(id)
        yahoo_df = yahoo_data(id).get_yahoo_quote()[::-1]
        yahoo_df.reset_index(inplace=True)
        yahoo_df.drop('index', axis=1, inplace=True)
        most_recent_day = datetime.strptime(str(yahoo_df['Date'][0])[:10],
                                            '%Y-%m-%d').day
        if most_recent_day != 1:
            yahoo_df = yahoo_df[0:]
            yahoo_df.reset_index(inplace=True)
            yahoo_df.drop('index', axis=1, inplace=True)
        # extracting all dates in the dataframe adding these into the dates array
        self.dates.extend([str(yahoo_df['Date'][index])[:10]
                           for index in range(0, len(yahoo_df))])
        # extracting all Adj close in yahoo finance
        self.values.extend([float(yahoo_df['Adj Close'][index])
                            for index in range(0, len(yahoo_df))])


class Dataset:
    """
    Contains the series id to fetech data from yahoo finance and fred API
    """

    def __init__(self):
        self.fred_series_ids = {'Non-farm_Payrolls': 'PAYEMS',
                                'Civilian_Unemployment_Rate': 'UNRATE',
                                'Effective_Fed_Funds': 'FEDFUNDS',
                                'CPI_All_Items': 'CPIAUCSL',
                                '10Y_Treasury_Rate': 'GS10',
                                '5Y_Treasury_Rate': 'GS5',
                                '3_Month_T-Bill_Rate': 'TB3MS',
                                'IPI': 'INDPRO'}
        self.yahoo_series_ids = {'S&P_500_Index': '^GSPC'}

    def get_yahoo_data(self):
        for series_id in self.yahoo_series_ids.keys():
            stock_data = yahoo_data(self.yahoo_series_ids[series_id]).get_yahoo_quote()[::-1]

        return stock_data
