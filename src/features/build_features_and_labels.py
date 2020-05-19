"""
generating final datasets with labels
"""
import pandas as pd


class FinalizeDataset:
    final_df_output = pd.read_csv("Data/Raw_Data/final_raw_data.csv")

    def threevstwelvemonth_change(self,threemo, twelvemo):
        df = pd.DataFrame()
        df["diff"] = self.final_df_output[threemo] - self.final_df_output[twelvemo]
        return df

    # create comparison features that compares payrolls, s&p,ipi for 3 vs 12 months
    def create_comparison_features(self):
        self.final_df_output['Payrolls_3mo_vs_12mo'] = self.threevstwelvemonth_change('Non-farm_Payrolls_3_mo_annualised','Non-farm_Payrolls_12_month_pchg')
        self.final_df_output['IPI_3mo_vs_12mo'] = self.threevstwelvemonth_change('IPI_3_month_pchg','IPI_12_month_pchg')
        self.final_df_output['CPI_3mo_vs_12mo'] = self.threevstwelvemonth_change('CPI_All_Items_3_mo_annualised','CPI_All_Items_12_month_pchg')
        self.final_df_output.to_csv("Data/Raw_Data/final_features_comparisonfields.csv", index=False)



    # Function to create recession label
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
        # Add column 'recession'to indicate recession for the year '1'for recession happened and '0' otherwise
        row_no = len(self.final_df_output)
        self.final_df_output['Recession'] = [0] * row_no

        for recession in US_recessions:
            end_condition = (US_recessions[recession]['End'] >= self.final_df_output['Date'])
            start_condition = (self.final_df_output['Date']  >= US_recessions[recession]['Start'])
            self.final_df_output.loc[end_condition & start_condition, 'Recession'] = 1

     # Function to create recession label for recession in 6 months , 12 months and 24 months
    def create_recession_6mo_12mo_24mo_label(self):
        # create columns for recession in 6moths, 12 months and 24 months
        row_no = len(self.final_df_output)
        self.final_df_output['Recession_in_6mo'] = [0] * row_no
        self.final_df_output['Recession_in_12mo'] = [0] * row_no
        self.final_df_output['Recession_in_24mo'] = [0] * row_no

        # If recession label is 1, add 1 to Recession_in_6mo,Recession_in_12mo,Recession_in_24mo

        for index in range(0, len(self.final_df_output)):
            if self.final_df_output['Recession'][index] == 1:
                self.final_df_output.loc[min(index + 6, len(self.final_df_output) - 1),'Recession_in_6mo'] = 1
                self.final_df_output.loc[min(index + 12, len(self.final_df_output) - 1),'Recession_in_12mo'] = 1
                self.final_df_output.loc[min(index + 24, len(self.final_df_output) - 1),'Recession_in_24mo'] = 1


    def create_final_dataset(self):
        self.create_comparison_features()
        self.create_recessionlabel()
        self.create_recession_6mo_12mo_24mo_label()
        print('Dataset with all labels added')
        self.final_df_output.to_csv("Data/final_features.csv",index=False)
