"""
generating final datasets with labels
"""
import pandas as pd


class FinalizeDataset:
    """
    final data
    """

    def __init(self):
        self.secondary_df_output = pd.DataFrame()
        self.final_df_output = pd.DataFrame()

    def generate_features(self):

        payrolls_3_mo_vs_12mo = (self.secondary_df_output['farm_Payrolls_3_mo_annualised']
                                 - self.secondary_df_output['Non-farm_Payrolls_3_month_pchg'])
        CPI_3_mo_vs_12mo = (self.secondary_df_output['CPI_All_Items_3_mo_annualised']
                            - self.secondary_df_output['CPI_All_Items_12_mo_annualised'])
        SP500_3_mo_vs_12mo = (self.secondary_df_output['S&P_500_Index_3_mo_annualised']
                              - self.secondary_df_output['S&P_500_Index_12_mo_annualised'])
        IPI_3_mo_vs_12mo = (self.secondary_df_output['IPI_3_mo_annualised']
                            - self.secondary_df_output['IPI_12_mo_annualised'])

        self.final_df_output['Payrolls_3_mo_vs_12mo'] = payrolls_3_mo_vs_12mo
        self.final_df_output['CPI_3_mo_vs_12mo'] = CPI_3_mo_vs_12mo
        self.final_df_output['S&P_500_3_mo_vs_12mo'] = SP500_3_mo_vs_12mo
        self.final_df_output['IPI_3_mo_vs_12mo'] = IPI_3_mo_vs_12mo

    def data_label_output(self):
        """
        Labels the various outputs.
        """
        # https://www.nber.org/cycles.html
        us_recessions = {'1': {'Begin': '1957-08-01', 'End': '1958-04-01'},
                         '2': {'Begin': '1960-04-01', 'End': '1961-02-01'},
                         '3': {'Begin': '1969-12-01', 'End': '1970-11-01'},
                         '4': {'Begin': '1973-11-01', 'End': '1975-03-01'},
                         '5': {'Begin': '1980-01-01', 'End': '1980-07-01'},
                         '6': {'Begin': '1981-07-01', 'End': '1982-11-01'},
                         '7': {'Begin': '1990-07-01', 'End': '1991-03-01'},
                         '8': {'Begin': '2001-03-01', 'End': '2001-11-01'},
                         '9': {'Begin': '2007-12-01', 'End': '2009-06-01'}}

        observation_count = len(self.final_df_output)
        self.final_df_output['Recession'] = [0] * observation_count
        self.final_df_output['Recession_in_6mo'] = [0] * observation_count
        self.final_df_output['Recession_in_12mo'] = [0] * observation_count
        self.final_df_output['Recession_in_24mo'] = [0] * observation_count
        self.final_df_output['Recession_within_6mo'] = [0] * observation_count
        self.final_df_output['Recession_within_12mo'] = [0] * observation_count
        self.final_df_output['Recession_within_24mo'] = [0] * observation_count

        for recession in us_recessions:
            end_condition = (us_recessions[recession]['End']
                             >= self.final_df_output['Date'])
            begin_condition = (self.final_df_output['Date']
                               >= us_recessions[recession]['Begin'])
            self.final_df_output.loc[end_condition & begin_condition, 'Recession'] = 1

        for index in range(0, len(self.final_df_output)):
            if self.final_df_output['Recession'][index] == 1:
                self.final_df_output.loc[min(index + 6, len(self.final_df_output) - 1),
                                         'Recession_in_6mo'] = 1
                self.final_df_output.loc[min(index + 12, len(self.final_df_output) - 1),
                                         'Recession_in_12mo'] = 1
                self.final_df_output.loc[min(index + 24, len(self.final_df_output) - 1),
                                         'Recession_in_24mo'] = 1
                self.final_df_output.loc[index: min(index + 6, len(self.final_df_output) - 1),
                'Recession_within_6mo'] = 1
                self.final_df_output.loc[index: min(index + 12, len(self.final_df_output) - 1),
                'Recession_within_12mo'] = 1
                self.final_df_output.loc[index: min(index + 24, len(self.final_df_output) - 1),
                'Recession_within_24mo'] = 1

    def create_final_dataset(self):
        """
        Creates and saves the final dataset.
        """
        print('\nCreating final dataset...')
        self.secondary_df_output = pd.read_csv("Data/Processed/finaldata.csv")
        self.secondary_df_output.sort_index(inplace=True)
        self.final_df_output = self.secondary_df_output
        self.generate_features()
        self.data_label_output()
        new_cols = ['Dates', 'Recession', 'Recession_in_6_month',
                    'Recession_in_12_month', 'Recession_in_24_month',
                    'Recession_within_6_month', 'Recession_within_12mo',
                    'Recession_within_24mo', 'Payrolls_3mo_pct_chg_annualized',
                    'Payrolls_12mo_pct_chg', 'Payrolls_3mo_vs_12mo',
                    'Unemployment_Rate', 'Unemployment_Rate_12mo_chg',
                    'Real_Fed_Funds_Rate', 'Real_Fed_Funds_Rate_12mo_chg',
                    'CPI_3mo_pct_chg_annualized', 'CPI_12mo_pct_chg',
                    'CPI_3mo_vs_12mo', '10Y_Treasury_Rate_12mo_chg',
                    '3M_Treasury_Rate_12mo_chg', '3M_10Y_Treasury_Spread',
                    '3M_10Y_Treasury_Spread_12mo_chg',
                    '5Y_10Y_Treasury_Spread', 'S&P_500_3mo_chg',
                    'S&P_500_12mo_chg', 'S&P_500_3mo_vs_12mo',
                    'IPI_3mo_pct_chg_annualized', 'IPI_12mo_pct_chg',
                    'IPI_3mo_vs_12mo']
        self.final_df_output = self.final_df_output[new_cols]
        print('Finished creating final dataset!')
        self.final_df_output.to_csv("Data/final_features.csv")
