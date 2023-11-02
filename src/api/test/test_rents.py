from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Profile, Rent
from api.test.demo_db import DemoDB
from api.test.firebase_login import get_test_user_client


class RentsAPITests(APITestCase):

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
        response = self.client.get('/api/v1/rents/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(f'/api/v1/users/{self.demo_db.p1.id}/rents/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rents_list_permission(self):
        """
        Ensure api return 403 if trying to get infos from other users.
        """
        response = self.auth_client.get(f'/api/v1/users/{self.demo_db.profile2.id}/rents/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rents_list(self):
        """
        Ensure rents list view works.
        """
        response = self.auth_client.get(f'/api/v1/users/{self.demo_db.profile1.id}/rents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

    def test_rent_create(self):
        """
        Ensure rent create view works.
        """
        response = self.auth_client.post('/api/v1/rents/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # owner is taken from logged user (jwt token)
        response = self.auth_client.post('/api/v1/rents/', {
            'product': self.demo_db.p3.id,
            'start_time': '2023-12-01T00:00:00Z',
            'end_time': '2023-12-02T00:00:00Z',
            'price': 40.00
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rent.objects.count(), 4)
        self.demo_db.r4c = Rent.objects.get(id=response.json()['id'])
        self.assertEqual(self.demo_db.r4c.payment_method, 'OPP')
        self.assertEqual(self.demo_db.r4c.price, 40)
        self.assertEqual(self.demo_db.r4c.status, 'pending')
