import pprint
import unittest

import requests


class APITestCase(unittest.TestCase):
    base_url = 'http://localhost:5000'

    def test_register(self):
        response = requests.post(self.base_url + '/register', json={
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)

    def get_token(self):
        response = requests.post(self.base_url + '/login', json={
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        return response.json()['user']['idToken']

    def test_upload_product(self):
        token = self.get_token()
        pprint.pprint(token)
        response = requests.post(self.base_url + '/upload_product', headers={
            'Authorization': token
        }, json={
            'product': 'Test Product'
        })
        self.assertEqual(response.status_code, 201)

    def test_user_products(self):
        token = self.get_token()
        response = requests.get(self.base_url + '/user_products', headers={
            'Authorization': token
        })
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    def test_delete_product(self):
        token = self.get_token()
        response = requests.delete(self.base_url + '/delete_product/-O6yolmVYAhsRX0bytlQ', headers={
            'Authorization': token
        })
        self.assertEqual(response.status_code, 204)

    def test_get_product(self):
        response = requests.get(self.base_url + '/product_info/-O6wLMaNoRm9978jsjyX')
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    def test_get_all_products(self):
        response = requests.get(self.base_url + '/all_products')
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    def test_update_product(self):
        token = self.get_token()
        response = requests.put(self.base_url + '/update_product/-O6wLMaNoRm9978jsjyX', headers={
            'Authorization': token
        }, json={
            'product': 'Matan Product'
        })
        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

    def test_search_product(self):
        search_query = 'Matan'
        response = requests.get(f'{self.base_url}/search_products?query={search_query}')

        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

        # Optionally, add more assertions based on expected results
        data = response.json()
        self.assertGreater(len(data), 0, "Expected at least one product to be returned")

    def test_filter_by_category(self):
        category = 'TEST1'
        response = requests.get(f'{self.base_url}/products_by_category/{category}')

        self.assertEqual(response.status_code, 200)
        pprint.pprint(response.json())

        # Optionally, add more assertions based on expected results
        data = response.json()
        self.assertGreater(len(data), 0, "Expected at least one product to be returned")


if __name__ == '__main__':
    unittest.main()
