from flask import Flask
import src.Data.retrieve_data as sk

app = Flask(__name__)


@app.route('/getData')
def get_data():
    data = sk.Dataset().get_yahoo_data()
    return data


if __name__ == '__main__':
    app.run()
