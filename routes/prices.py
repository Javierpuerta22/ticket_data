from flask import Blueprint, request, jsonify
from flask_cors import CORS

from models.model_data import DataManipulator
from models.model_csv import CSVconstructor, PDFFile
from .monthly import DataClass

prices = Blueprint('prices', __name__)
CORS(prices)


@prices.route('/prices/data/type', methods=['GET'])
def get_type():
    return jsonify(DataClass.get_types_of_products())


@prices.route('/prices/data/subtype', methods=['GET'])
def get_subtype():
    type = request.args.get('type')
    return jsonify(DataClass.get_subtypes_of_products(type))



@prices.route('/prices/data/timeline', methods=['POST'])
def get_timeline():
    product = request.json.get('product')
    return jsonify(DataClass.select_prices_timeline_by_product(product))