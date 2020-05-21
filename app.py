from flask import Flask
import src.Data.retrieve_data as sk
import src.Analysis.graph_api as gp
import src.Models.svm as svm
from flask import Flask
from flask_cors import CORS
from flask import request
app = Flask(__name__)
CORS(app)


@app.route('/getdata')
def get_data():
    res = {}
    try:
        data = sk.Dataset().combine_data()
        for i in data.keys():
            res[i] = i.values
        print(data)
    except:
        print("error")
    return res


@app.route('/selectFeature')
def feature_selection():
    try:
        data = sk.Dataset().calculation()
        print(data)


    except:
        print("error")
    return "success"


@app.route('/graph', methods=['GET'])
def get_graph_data():
    try:
        id = request.args.get("id")
        data = gp.feature_graph().graph_api_data(id)
        return data



    except:
        return ("error")


@app.route('/svm', methods=['GET'])
def get_svm():
    try:
        data = svm.svm_prediction().svm_model_prediction()
        return data
    except Exception as e:
        return (e)


if __name__ == '__main__':
    app.run(host=('0.0.0.0'), debug=True)
