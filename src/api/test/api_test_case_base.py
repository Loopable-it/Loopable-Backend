from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import Profile
from api.test.demo_db import DemoDB
from api.test.firebase_login import FirebaseTestUsers


class APITestCaseBase(APITestCase):

    def __init__(self, args):
        super().__init__(args)
        self.demo_db = None
        self.auth_client = None
        self.auth_client2 = None

    def setup_test_users_and_db(self):
        """
        Setup and ensure we can create a new User and the demo db.
        """
        # Create users
        self.auth_client = FirebaseTestUsers().get_test_user_client('USER1')
        response = self.auth_client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.auth_client2 = FirebaseTestUsers().get_test_user_client('USER2')
        response = self.auth_client2.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(Profile.objects.count(), 2)

        # Create categories and products
        self.demo_db = DemoDB()  # This is from demo_db.py
