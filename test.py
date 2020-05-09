import src.Data.retrieve_data as sk
import src.features.build_features_and_labels as feature
import json

# sk.Dataset().combine_data()
# sk.Dataset().calculation()
feature.FinalizeDataset().create_final_dataset()

# data = gp.feature_graph().graph_api_data()
# print(data)
