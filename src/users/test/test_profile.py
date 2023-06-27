from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Profile
from users.test.firebase_login import get_test_user_client


class UsersAPITests(APITestCase):

    def setUp(self):
        """
        Setup and ensure we can create a new User and Profile object.
        """
        self.auth_client = get_test_user_client('USER1')
        response = self.auth_client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_no_token(self):
        """
        Ensure api return 401 if no token is passed in the Authorization header.
        """
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_list(self):
        """
        Ensure profile list view works.
        """
        profile = Profile.objects.all()[0]

        response = self.auth_client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        profile.name = 'Alex'
        profile.lastname = 'Vellons'
        profile.save()

        # Test filters
        response = self.auth_client.get('/api/v1/users/', {'name': 'Alex'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.auth_client.get('/api/v1/users/', {'name': 'not-my-name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        response = self.auth_client.get('/api/v1/users/', {'lastname': 'Vellons'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.auth_client.get('/api/v1/users/', {'lastname': 'not-my-name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        all_filters = {'name': 'Alex', 'lastname': 'Vellons', 'type': 'STD', 'is_verified': False}
        response = self.auth_client.get('/api/v1/users/', all_filters)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.auth_client.get('/api/v1/users/', {'search': 'vellons'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_profile_detail(self):
        """
        Ensure profile detail view works.
        """
        profile = Profile.objects.all()[0]

        response = self.auth_client.get('/api/v1/users/{}/'.format(profile.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_update(self):
        """
        Ensure profile update view works.
        """
        profile = Profile.objects.all()[0]

        data = {'name': 'Alex', 'lastname': 'Vellons', 'type': 'BUS', 'is_verified': True}
        response = self.auth_client.patch('/api/v1/users/{}/'.format(profile.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_test = {
            'id': profile.id,
            'name': 'Alex',
            'lastname': 'Vellons',
            'type': 'STD',  # Not to update
            'is_verified': False,  # Not to update
            'sign_in_provider': 'password',
            'fcm_token': None,
            'allow_notifications': True,
        }
        assert response.json().items() >= resp_test.items()  # Check if all keys and values are in response
