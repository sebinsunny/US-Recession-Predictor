import re
from io import StringIO
import json
from datetime import datetime, timedelta
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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
        self.dates.extend(yahoo_df['Date'])
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
        self.df_without_all = pd.DataFrame()
        self.df_with_all = pd.DataFrame()

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


        print('Finished getting data from Fred API')

    def max_date(self):
        a = []
        for j in list(self.primary_output['Non-farm_Payrolls'].dates):
            if ((j >= self.start_date) and (j <= self.end_date)):
                a.append(j)
        return a

    def fetch_data_one(self, seriesid):
        mindate = []
        maxdate = []
        fred_series_ids = dict(self.fred_series_ids, **self.yahoo_series_ids)
        for i in fred_series_ids:
            if i == seriesid:
                continue
            mindate.append(min(self.primary_output[i].dates))
            maxdate.append(max(self.primary_output[i].dates))

        self.start_date = max(mindate)
        self.end_date = min(maxdate)
        df = pd.DataFrame()
        df['Date'] = self.max_date()
        for series_name in list(fred_series_ids):
            a = []
            k = 0

            if series_name == seriesid:
                continue
            for j in list(self.primary_output[series_name].dates):
                if ((j >= self.start_date) and (j <= self.end_date)):
                    a.append(self.primary_output[series_name].values[k])
                k = k + 1
            df[series_name] = a
        return df

    #
    def combine_data(self):
        self.get_yahoo_data()
        self.get_fred_data()
        self.df_without_all = self.fetch_data_one('House_price_index')
        self.df_without_all.to_csv("Data/Datasets/raw_data_with_all.csv", index=False)
        self.df_with_all = self.fetch_data_one('all')
        self.df_with_all.to_csv("Data/Datasets/raw_data_with_house_price.csv", index=False)
        return self.primary_output

    def get_correlation(self):
        df_correl = pd.read_csv("Data/Processed/finaldata.csv")
        df_correl = df_correl.drop('Date',1)
        fig, ax = plt.subplots()
        sns.heatmap(df_correl.corr(method='pearson'), annot=True, fmt='.1f',
                    cmap=plt.get_cmap('coolwarm'), cbar=False, ax=ax)
        ax.set_yticklabels(ax.get_yticklabels(), rotation="horizontal")
        plt.savefig('result.png', bbox_inches='tight', pad_inches=0.0)

        #
        # corr = df_correl.corr()
        # print(corr)
        # corr.style.background_gradient(cmap='coolwarm')
        #
        # plt.matshow(corr)
        # plt.show()

        # print(df_correl.corr())

    # Add recession labels to the dataset
     def recession_label_add(self):
         create_recessionlabel()
         create_recession_6mo_12mo_24mo_label()

    #Function to create recession label
    def create_recessionlabel(self):

        US_recessions = {'1': {'Start': '1957-08-01', 'End': '1958-04-01'},
                         '2': {'Start': '1960-04-01', 'End': '1961-02-01'},
                         '3': {'Start': '1969-12-01', 'End': '1970-11-01'},
                         '4': {'Start': '1973-11-01', 'End': '1975-03-01'},
                         '5': {'Start': '1980-01-01', 'End': '1980-07-01'},
                         '6': {'Start': '1981-07-01', 'End': '1982-11-01'},
                         '7': {'Start': '1990-07-01', 'End': '1991-03-01'},
                         '8': {'Start': '2001-03-01', 'End': '2001-11-01'},
                         '9': {'Start': '2007-12-01', 'End': '2009-06-01'}}
        #Add column 'recession'to indicate recession for the year '1'for recession happened and '0' otherwise
        row_no = len(self.final_df_output)
        self.final_df_output['Recession'] = [0] * row_no

        for recession in US_recessions:
            end_condition = (US_recessions[recession]['End']
                             >= self.final_df_output['Dates'])
            start_condition = (self.final_df_output['Dates']
                               >= US_recessions[recession]['Begin'])
            self.final_df_output.loc[end_condition & start_condition, 'Recession'] = 1

    #Function to create recession label for recession in 6 months , 12 months and 24 months
    def create_recession_6mo_12mo_24mo_label(self):
        #create columns for recession in 6moths, 12 months and 24 months
        row_no = len(self.final_df_output)
        self.final_df_output['Recession_in_6mo'] = [0] * row_no
        self.final_df_output['Recession_in_12mo'] = [0] * row_no
        self.final_df_output['Recession_in_24mo'] = [0] * row_no

        #If recession label is 1, add 1 to Recession_in_6mo,Recession_in_12mo,Recession_in_24mo

        for index in range(0, len(self.final_df_output)):
            if self.final_df_output['Recession'][index] == 1:
                self.final_df_output.loc[min(index + 6, len(self.final_df_output) - 1),
                                         'Recession_in_6mo'] = 1
                self.final_df_output.loc[min(index + 12, len(self.final_df_output) - 1),
                                         'Recession_in_12mo'] = 1
                self.final_df_output.loc[min(index + 24, len(self.final_df_output) - 1),
                                         'Recession_in_24mo'] = 1


    def calculation(self):
        #self.combine_data()
        df_recession = pd.read_csv("Data/Datasets/raw_data_with_all.csv")
        fields_to_be_annaulised = ['Non-farm_Payrolls', 'CPI_All_Items', 'IPI', 'S&P_500_Index']
        fields_to_per_chg = ['Non-farm_Payrolls', 'Civilian_Unemployment_Rate', 'CPI_All_Items', 'S&P_500_Index', 'IPI']

        df_processed_data = df_recession.truncate(after=len(df_recession) - 13)
        final = pd.DataFrame()

        # annualisation
        for i in fields_to_be_annaulised:
            fieldname = i + '_3_mo_annualised'
            df_processed_data[fieldname] = Dataprocessing.annualise_data(df_recession, i, 3)

        # percentage_change
        for i in fields_to_per_chg:
            fieldname = i + '_3_month_pchg'

            df_processed_data[fieldname] = Dataprocessing.percentage_chg(df_recession, i, 3)
            fieldname = i + '_12_month_pchg'
            df_processed_data[fieldname] = Dataprocessing.percentage_chg(df_recession, i, 12)
        df_processed_data = df_processed_data.drop(['Civilian_Unemployment_Rate_3_month_pchg'], axis=1)
        df_processed_data.to_csv('Data/Processed/finaldata.csv', index=False)
        return df_processed_data


#Process data
class Dataprocessing:
    def annualise_data(df, seriesid, month):
        annualised_data = []
        for i in range(0, len(df) - 12):
            annualised_data.append((df[seriesid][i] / df[seriesid][i + 3]) ** (12 / (month)))
        return annualised_data

    def percentage_chg(df, seriesid, month):
        per_chg = []
        for i in range(0, len(df) - 12):
            per_chg.append((df[seriesid][i] / df[seriesid][i + month]) - 1)
        return per_chg
