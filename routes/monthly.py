from flask import Blueprint, request, jsonify
from flask_cors import CORS

from models.model_data import DataManipulator
from models.model_csv import CSVconstructor, PDFFile

monthly = Blueprint('monthly', __name__)
CORS(monthly)

DataClass = DataManipulator('./data/csv/data.csv')


@monthly.route('/monthly/data', methods=['GET'])
def get_month():
    return jsonify(DataClass.stadistics_actual_month())