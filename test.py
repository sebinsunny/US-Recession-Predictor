import src.Data.retrieve_data as sk
import src.features.build_features_and_labels as feature
import json

# d = sk.Dataset().calculation()
fields_to_be_annaulised = ['Non-farm_Payrolls', 'CPI_All_Items', 'IPI', 'S&P_500_Index']
fields_to_per_chg = ['Non-farm_Payrolls', 'Civilian_Unemployment_Rate', 'CPI_All_Items', 'IPI', 'S&P_500_Index']
for i, j in zip(fields_to_be_annaulised, fields_to_per_chg):
    print(i, j)
import src.Analysis.graph_api as gp

data = gp.feature_graph().graph_api_data()
print(data)
