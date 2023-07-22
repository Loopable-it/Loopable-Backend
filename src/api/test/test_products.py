from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Profile, ProductCategory, Product
from api.test.firebase_login import get_test_user_client, get_profile


class ProductsAPITests(APITestCase):

    def setUp(self):
        """
        Setup and ensure we can create a new User, Profile and Products object.
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
        self.profile1 = get_profile('USER1')
        self.profile2 = get_profile('USER2')
        ProductCategory.objects.create(id=1, name='Category 1', description='Category 1 description')
        ProductCategory.objects.create(id=2, name='Category 2', description='Category 2 description')
        ProductCategory.objects.create(id=3, name='Category 3', description='Category 3 description')
        self.p1 = Product.objects.create(name='Product 1 ABC', description='Product 1 description',
                                         owner=self.profile1, price=10.00, category_id=1)
        self.p2 = Product.objects.create(name='Product 2 BCD', description='Product 2 description',
                                         owner=self.profile1, price=20.00, category_id=2)
        self.p3 = Product.objects.create(name='Product 3 XYZ', description='Product 3 description',
                                         owner=self.profile2, price=30.00, category_id=2)

    def test_no_token(self):
        """
        Ensure api return 401 if no token is passed in the Authorization header.
        """
        response = self.client.get('/api/v1/product-category/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_category_list(self):
        """
        Ensure product category list view works.
        """
        response = self.auth_client.get('/api/v1/product-category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

        # Test filters
        response = self.auth_client.get('/api/v1/product-category/', {'id': '2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.auth_client.get('/api/v1/product-category/', {'name': 'Category 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_product_list(self):
        """
        Ensure product list view works.
        """
        response = self.auth_client.get('/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 3)

        # Test filters
        response = self.auth_client.get('/api/v1/products/', {'id': self.p1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

        response = self.auth_client.get('/api/v1/products/', {'name': 'Product 1 ABC'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

        response = self.auth_client.get('/api/v1/products/', {'category': '2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

        response = self.auth_client.get('/api/v1/products/', {'owner': self.profile1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

        response = self.auth_client.get('/api/v1/products/', {'search': 'BC'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)
