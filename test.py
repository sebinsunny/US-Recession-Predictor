import src.Data.retrieve_data as sk
from src.features import build_features_and_labels as feature
import src.Models.recession_models as svm

# sk.Dataset().combine_data()
# sk.Dataset().calculation()
# feature.FinalizeDataset().create_final_dataset()
#
# # data = gp.feature_graph().graph_api_data()
# # print(data)

svm.recession_models().models('sv')
print("data")
