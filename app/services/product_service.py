from firebase_admin import auth, db
from app.utils.helpers import handle_exception


class ProductService:

    @staticmethod
    def upload_product(data, user_token):
        product_data = data.get('product')

        if not product_data or not user_token:
            return {"error": "Product data and authorization token are required", "status": 400}

        try:
            decoded_token = auth.verify_id_token(user_token)
            user_id = decoded_token['uid']
            product_ref = db.reference('products').push({
                'product': product_data,
                'user_id': user_id
            })
            return {"message": "Product uploaded", "product_id": product_ref.key, "status": 201}
        except Exception as e:
            return handle_exception(e)

    @staticmethod
    def get_user_products(user_token):
        if not user_token:
            return {"error": "Authorization token is required", "status": 400}

        try:
            decoded_token = auth.verify_id_token(user_token)
            user_id = decoded_token['uid']
            products_ref = db.reference('products')
            products = products_ref.get()

            if not products:
                return {"message": "No products found", "status": 404}

            filtered_products = [
                {"id": key, "product": value.get("product"), "user_id": value.get("user_id")}
                for key, value in products.items() if value.get('user_id') == user_id
            ]

            if not filtered_products:
                return {"message": "No products found for this user", "status": 404}

            return filtered_products, 200
        except Exception as e:
            return handle_exception(e)

    @staticmethod
    def delete_product(product_id, user_token):
        if not user_token:
            return {"error": "Authorization token is required", "status": 400}

        try:
            decoded_token = auth.verify_id_token(user_token)
            user_id = decoded_token['uid']
            product_ref = db.reference('products').child(product_id)
            product = product_ref.get()

            if not product:
                return {"message": "Product not found", "status": 404}

            if product.get('user_id') == user_id:
                product_ref.delete()
                return {"message": "Product deleted", "status": 204}
            else:
                return {"error": "Unauthorized", "status": 401}
        except Exception as e:
            return handle_exception(e)

    @staticmethod
    def get_product_info(product_id):
        try:
            product_ref = db.reference('products').child(product_id)
            product = product_ref.get()

            if not product:
                return {"message": "Product not found", "status": 404}

            return product, 200
        except Exception as e:
            return handle_exception(e)

    @staticmethod
    def get_all_products():
        try:
            products = db.reference('products').get()
            if not products:
                return {"message": "No products found", "status": 404}
            return products, 200
        except Exception as e:
            return handle_exception(e)

    @staticmethod
    def update_product(product_id, data, user_token):
        product_data = data.get('product')

        if not product_data or not user_token:
            return {"error": "Product data and authorization token are required", "status": 400}

        try:
            decoded_token = auth.verify_id_token(user_token)
            user_id = decoded_token['uid']
            product_ref = db.reference('products').child(product_id)
            product = product_ref.get()

            if not product:
                return {"message": "Product not found", "status": 404}

            if product.get('user_id') == user_id:
                product_ref.update({'product': product_data})
                return {"message": "Product updated", "status": 200}
            else:
                return {"error": "Unauthorized", "status": 401}
        except Exception as e:
            return handle_exception(e)

    @staticmethod
    def search_products(query):
        if not query:
            return {"error": "Query parameter is required", "status": 400}

        try:
            products_ref = db.reference('products')
            all_products = products_ref.get()

            if not all_products:
                return {"message": "No products found", "status": 404}

            filtered_products = [
                {"id": key, "product": value.get("product")}
                for key, value in all_products.items() if query.lower() in value.get("product", "").lower()
            ]

            if not filtered_products:
                return {"message": "No products found matching query", "status": 404}

            return filtered_products, 200
        except Exception as e:
            return handle_exception(e)

    @staticmethod
    def get_products_by_category(category_name):
        if not category_name:
            return {"error": "Category name is required", "status": 400}

        try:
            products_ref = db.reference('products')
            all_products = products_ref.get()

            if not all_products:
                return {"message": "No products found", "status": 404}

            filtered_products = [
                {"id": key, "product": value.get("product")}
                for key, value in all_products.items() if category_name.lower() == value.get("category", "").lower()
            ]

            if not filtered_products:
                return {"message": "No products found in this category", "status": 404}

            return filtered_products, 200
        except Exception as e:
            return handle_exception(e)
