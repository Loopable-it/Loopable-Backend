from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Profile, Product
from api.test.demo_db import DemoDB
from api.test.firebase_login import get_test_user_client


class ProductsAPITests(APITestCase):

    def setUp(self):
        """
        Setup and ensure we can create a new User and the demo db.
        """
        # Create users
        self.auth_client = get_test_user_client('USER1')
        response = self.auth_client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.auth_client2 = get_test_user_client('USER2')
        response = self.auth_client2.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Profile.objects.count(), 2)

        # Create categories and products
        self.demo_db = DemoDB()

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
