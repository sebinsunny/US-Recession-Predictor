import src.Data.retrieve_data as sk
import datetime
import src.features.build_features_and_labels as feature

import json
#
# # d = sk.Dataset().calculation()
# fields_to_be_annaulised = ['Non-farm_Payrolls', 'CPI_All_Items', 'IPI', 'S&P_500_Index']
# fields_to_per_chg = ['Non-farm_Payrolls', 'Civilian_Unemployment_Rate', 'CPI_All_Items', 'IPI', 'S&P_500_Index']
# for i, j in zip(fields_to_be_annaulised, fields_to_per_chg):
#     print(i, j)
# import src.Analysis.graph_api as gp
#
# data = gp.feature_graph().graph_api_data()
# print(data)
# import requests
# import json
# import pandas as pd
#
# # import requests
# # from bs4 import BeautifulSoup
# # url = "https://www.realestateview.com.au/portal/search/?sort=&viewAlertId=&frequency=&smt=Sold&ftl=&loc=&regions=Melbourne%7CVIC&pt=&iss=True"
# # page_request = requests.get(url)
# data = sk.Dataset().get_yahoo_data()
# date = list(map(lambda x: x.strftime('%Y-%m-%d'), data['S&P_500_Index'].dates))
# print((date))
#
# print(data)
# soup = BeautifulSoup(data,"html.parser")
#
# price,address,dates=[],[],[]
# for content in soup.find_all('div', {'class': 'content'}):
#     for i in content.find_all('div', {'class': 'list-price'}):
#         price.append(i.text)
#     for i in content.find_all('div', {'class': 'list-address'}):
#         address.append(i.text)
#     for sold in content.find_all('div', {'class': 'desktop flag-sold'}):
#         for i in sold.find_all('span', {'class': 'sold-date-text'}):
#             dates.append(i.text)
#
#
# df = pd.DataFrame(data={'price':price,'address':address,'sold_date':dates})
# df.to_csv("file.csv",index=False)

# from sklearn.impute import SimpleImputer
# import numpy as np
#
# imputer = SimpleImputer(missing_values = np.nan, strategy = 'mean')
# imputer.fit([[7, 2, 3], [4, np.nan, 6], [10, 5, 9]])


# import requests, threading
#
#
# proxies = open('proxies.txt', 'r').read().splitlines()
# url = input('Enter the url with its protocol -> ')
# timeout = int(input('Enter the timeout in seconds (number/int) -> '))
# tc = int(input('Thread count -> '))
#
# def cthread():
#     while len(proxies) > 0:
#         proxy = proxies.pop(0)
#         try:
#             requests.get(url, proxies={'https':proxy}, timeout=timeout)
#             print(proxy, '< GOOD PROXY')
#             with open('Working proxies.txt', 'a') as proxywork:
#                 proxywork.write(proxy + '\n')
#                 proxywork.flush()
#         except:
#             print(proxy, ' > BAD')
#
# for i in range(tc):
#     threading.Thread(target=cthread).start()
