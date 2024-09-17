import pprint

from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService

product_bp = Blueprint('product_bp', __name__)


@product_bp.route('/upload_product', methods=['POST'])
def upload_product():
    data = request.json
    user_token = request.headers.get('Authorization')
    result = ProductService.upload_product(data, user_token)
    return jsonify(result), result['status']


@product_bp.route('/user_products', methods=['GET'])
def user_products():
    user_token = request.headers.get('Authorization')
    result = ProductService.get_user_products(user_token)
    return jsonify(result[0]), result[1]


@product_bp.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    user_token = request.headers.get('Authorization')
    result = ProductService.delete_product(product_id, user_token)
    return jsonify(result), result['status']


@product_bp.route('/product_info/<product_id>', methods=['GET'])
def product_info(product_id):
    result = ProductService.get_product_info(product_id)
    return jsonify(result[0]), result[1]


@product_bp.route('/all_products', methods=['GET'])
def all_products():
    result = ProductService.get_all_products()
    return jsonify(result[0]), result[1]


@product_bp.route('/update_product/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    user_token = request.headers.get('Authorization')
    result = ProductService.update_product(product_id, data, user_token)
    return jsonify(result[0]), result[1]


@product_bp.route('/search_products', methods=['GET'])
def search_products():
    query = request.args.get('query')
    result = ProductService.search_products(query)
    return jsonify(result[0]), result[1]


@product_bp.route('/products_by_category/<category_name>', methods=['GET'])
def products_by_category(category_name):
    result = ProductService.get_products_by_category(category_name)
    return jsonify(result[0]), result[1]
