from flask import Flask
import src.Data.retrieve_data as sk
import src.Analysis.graph_api as gp
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/getData')
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


@app.route('/graph')
def get_graph_data():
    try:
        data = gp.feature_graph().graph_api_data()
        print(data)


    except:
        print("error")
    return data


if __name__ == '__main__':
    app.run()
