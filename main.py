import json
import pprint

import firebase_admin
from firebase_admin import credentials, db, auth
from flask import Flask, request, jsonify
import pyrebase

# Initialize Flask app
app = Flask(__name__)

# Firebase Admin SDK setup (for secure admin operations)
cred = credentials.Certificate('secret.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://productmanagement-a2e14-default-rtdb.firebaseio.com/'
})

# Pyrebase configuration
config = {
    "apiKey": "AIzaSyBlH3AbKqjX7jrT7ZUvug34MB2_MiRq0dU",
    "authDomain": "productmanagement-a2e14.firebaseapp.com",
    "databaseURL": "https://productmanagement-a2e14-default-rtdb.firebaseio.com",
    "projectId": "productmanagement-a2e14",
    "storageBucket": "productmanagement-a2e14.appspot.com",
    "messagingSenderId": "1033785289784",
    "appId": "1:1033785289784:web:7e4b8c7f1f9f7a5f4a4e6f",
    "measurementId": "G-2J1J6V5X6Z"
}
firebase = pyrebase.initialize_app(config)
auth_pyrebase = firebase.auth()


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        # Create user in Firebase Authentication
        user = auth.create_user(email=email, password=password)
        # Store additional user info in Realtime Database
        user_ref = db.reference('users/' + user.uid)
        user_ref.set({'email': email})
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        user = auth_pyrebase.sign_in_with_email_and_password(email, password)
        return jsonify({"message": "User logged in successfully", "user": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/upload_product', methods=['POST'])
def upload_product():
    data = request.json
    user_token = request.headers.get('Authorization')
    product_data = data.get('product')

    if not product_data or not user_token:
        return jsonify({"error": "Product data and authorization token are required"}), 400

    try:
        decoded_token = auth.verify_id_token(user_token)
        user_id = decoded_token['uid']
        product_ref = db.reference('products').push({
            'product': product_data,
            'user_id': user_id
        })
        return jsonify({"message": "Product uploaded", "product_id": product_ref.key}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/user_products', methods=['GET'])
def user_products():
    user_token = request.headers.get('Authorization')

    if not user_token:
        return jsonify({"error": "Authorization token is required"}), 400

    try:
        decoded_token = auth.verify_id_token(user_token)
        user_id = decoded_token['uid']
        products_ref = db.reference('products')
        products = products_ref.get()

        if not products:
            return jsonify({"message": "No products found"}), 404

        filtered_products = [
            {
                "id": key,
                "product": value.get("product"),
                "user_id": value.get("user_id")
            }
            for key, value in products.items() if value.get('user_id') == user_id
        ]

        if not filtered_products:
            return jsonify({"message": "No products found for this user"}), 404

        return jsonify(filtered_products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    user_token = request.headers.get('Authorization')

    if not user_token:
        return jsonify({"error": "Authorization token is required"}), 400

    try:
        decoded_token = auth.verify_id_token(user_token)
        user_id = decoded_token['uid']
        product_ref = db.reference('products').child(product_id)
        product = product_ref.get()

        if not product:
            return jsonify({"message": "Product not found"}), 404

        if product.get('user_id') == user_id:
            product_ref.delete()
            return jsonify({"message": "Product deleted"}), 204
        else:
            return jsonify({"error": "Unauthorized"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/product_info/<product_id>', methods=['GET'])
def product_info(product_id):
    try:
        product_ref = db.reference('products').child(product_id)
        product = product_ref.get()

        if not product:
            return jsonify({"message": "Product not found"}), 404

        return jsonify(product), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/all_products', methods=['GET'])
def all_products():
    try:
        products = db.reference('products').get()
        if not products:
            return jsonify({"message": "No products found"}), 404
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/update_product/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    user_token = request.headers.get('Authorization')
    product_data = data.get('product')

    if not product_data or not user_token:
        return jsonify({"error": "Product data and authorization token are required"}), 400

    try:
        decoded_token = auth.verify_id_token(user_token)
        user_id = decoded_token['uid']
        product_ref = db.reference('products').child(product_id)
        product = product_ref.get()

        if not product:
            return jsonify({"message": "Product not found"}), 404

        if product.get('user_id') == user_id:
            product_ref.update({'product': product_data})
            return jsonify({"message": "Product updated"}), 200
        else:
            return jsonify({"error": "Unauthorized"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/search_products', methods=['GET'])
def search_products():
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        products_ref = db.reference('products')
        all_products = products_ref.get()

        if not all_products:
            return jsonify({"message": "No products found"}), 404

        matching_products = [
            {
                "id": key,
                "product": value.get("product"),
                "user_id": value.get("user_id")
            }
            for key, value in all_products.items() if query.lower() in value.get('product', '').lower()
        ]

        if not matching_products:
            return jsonify({"message": "No products match the query"}), 404

        return jsonify(matching_products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/products_by_category/<category_name>', methods=['GET'])
def products_by_category(category_name):
    if not category_name:
        return jsonify({"error": "Category name is required"}), 400

    try:
        products_ref = db.reference('products')
        products = products_ref.get()

        if not products:
            return jsonify({"message": "No products found"}), 404

        matching_products = [
            {
                "id": key,
                "product": value.get("product"),
                "user_id": value.get("user_id"),
                "category": value.get("category"),
            }
            for key, value in products.items() if category_name.lower() == value.get('category', '').lower()
        ]

        if not matching_products:
            return jsonify({"message": "No products found in this category"}), 404

        return jsonify(matching_products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
