from rest_framework import status

from api.models import Product
from api.test.api_test_case_base import APITestCaseBase


class ProductsAPITests(APITestCaseBase):

    def setUp(self):
        """
        Setup and ensure we can create a new User and the demo db.
        This method is called before each test.
        """
        self.setup_test_users_and_db()  # This is from api_test_case_base.py

    def test_no_token(self):
        """
        Ensure api return 401 if no token is passed in the Authorization header.
        """
        response = self.client.get('/api/v1/product-categories/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_category_list(self):
        """
        Ensure product category list view works.
        """
        response = self.auth_client.get('/api/v1/product-categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

        # Test filters
        response = self.auth_client.get('/api/v1/product-categories/', {'id': '2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.auth_client.get('/api/v1/product-categories/', {'name': 'Category 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_product_list(self):
        """
        Ensure product list view works.
        """
        response = self.auth_client.get('/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 4)

        # Test filters
        response = self.auth_client.get('/api/v1/products/', {'id': self.demo_db.p1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

        response = self.auth_client.get('/api/v1/products/', {'name': 'Product 1 ABC'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

        response = self.auth_client.get('/api/v1/products/', {'category': '2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 3)

        response = self.auth_client.get('/api/v1/products/', {'active': 'false'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

        response = self.auth_client.get('/api/v1/products/', {'stock_quantity': '3'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

        response = self.auth_client.get('/api/v1/products/', {'owner': self.demo_db.profile1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

        response = self.auth_client.get('/api/v1/products/', {'owner': 'not-an-owner'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.auth_client.get('/api/v1/products/', {'search': 'BC'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

    def test_product_create(self):
        """
        Ensure product create view works.
        """
        response = self.auth_client.post('/api/v1/products/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # owner is taken from logged user (jwt token)
        response = self.auth_client.post('/api/v1/products/', {
            'name': 'Product 5',
            'description': 'Product 5 description',
            'price': 40.00,
            'category': 3,
            'latitude': 40.0,
            'longitude': 40.0,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 5)
        self.demo_db.p5c = Product.objects.get(name='Product 5')
        self.assertEqual(self.demo_db.p5c.owner.id, self.demo_db.profile1.id)  # Check if owner is taken from logged
        self.assertEqual(self.demo_db.p5c.active, True)
        self.assertEqual(self.demo_db.p5c.stock_quantity, 1)
        self.assertEqual(self.demo_db.p5c.category.id, 3)

    def test_product_update(self):
        """
        Ensure product update view works.
        """
        data = {
            'name': 'Product prova',
            'description': 'Product prova description',
            'price': 40.00,
            'category': 2,
            'latitude': 50.0,
            'longitude': 50.0,
            'owner': '1234'
        }

        response = self.auth_client.patch(f'/api/v1/products/{self.demo_db.p1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = Product.objects.get(id=self.demo_db.p1.id)
        self.assertEqual(updated_product.name, 'Product prova')
        self.assertEqual(updated_product.description, 'Product prova description')
        self.assertEqual(updated_product.category.id, 2)
        self.assertEqual(updated_product.price, 40.00)
        self.assertEqual(updated_product.latitude, 50.0)
        self.assertEqual(updated_product.longitude, 50.0)
        self.assertEqual(updated_product.owner.id, self.demo_db.profile1.id)

    def test_product_update_permission(self):
        """
        Ensure product update view works only for the owner.
        """
        data = {'name': 'Product prova', 'description': 'Product prova description'}
        response = self.auth_client2.patch(f'/api/v1/products/{self.demo_db.p1.id}/', data)  # USER2 try to update USER1
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
