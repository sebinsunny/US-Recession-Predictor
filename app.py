from flask import Flask
import src.Data.retrieve_data as sk
import src.Analysis.graph_api as gp
import src.Models.recession_models as m
#import src.features.build_features_and_labels as feature
from flask import Flask
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)


@app.route('/getdata')
def get_data():
    try:
        sk.Dataset().combine_data()
        sk.Dataset().calculation()
        feature.FinalizeDataset().create_final_dataset()
        return "success"
    except Exception as e:
        return (e)

@app.route('/house_price')
def houseprice():
    try:
        market = request.args.get("m")
        sports_facility= request.args.get("sp")
        population = request.args.get("pop")
        school = request.args.get("sch")
        hospital = request.args.get("hosp")
        distance = request.args.get("dist")
        room = request.args.get("ro")
        price=m.recession_models().house_price(market,sports_facility,population,school,hospital,distance,room)
        return price
    except Exception as e:
        return (e)


@app.route('/graph', methods=['GET'])
def get_graph_data():
    try:
        id = request.args.get("id")
        data = gp.feature_graph().graph_api_data(id)
        return data
    except:
        return ("error")


@app.route('/model', methods=['GET'])
def get_svm():
    try:
        id = request.args.get("id")
        data = m.recession_models().models(id)
        return data
    except Exception as e:
        return (e)


if __name__ == '__main__':
    app.run(host=('0.0.0.0'), debug=True)
