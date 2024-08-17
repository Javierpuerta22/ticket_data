import flask
from flask import request, jsonify
from flask_cors import CORS

from models.model_data import DataManipulator



app = flask.Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')
CORS(app)
app.config["DEBUG"] = True


DataClass = DataManipulator('./data/csv/data.csv')

@app.route('/get_month', methods=['GET'])
def get_month():
    return jsonify(DataClass.group_by_month())

@app.route('/get_week', methods=['GET'])
def get_weekday():
    return jsonify(DataClass.group_by_weekday())

@app.route('/get_tipo', methods=['GET'])
def get_tipo():
    return jsonify(DataClass.group_by_tipo())



if __name__ == '__main__':
    app.run(debug=True, port=8000)