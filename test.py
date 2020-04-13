import src.Data.retrieve_data as sk
import json
d = sk.Dataset().get_yahoo_data()
print(d['Australia'].dates,d['Australia'].values)

