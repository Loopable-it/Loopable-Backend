from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Profile
from api.test.firebase_login import get_test_user_client


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
        response = self.auth_client.get('/api/v1/users/', {'id': profile.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.auth_client.get('/api/v1/users/', {'id': 'not-my-id'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        response = self.auth_client.get('/api/v1/users/', {'name': 'Alex'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.auth_client.get('/api/v1/users/', {'name': 'not-my-name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        response = self.auth_client.get('/api/v1/users/', {'lastname': 'Vellons'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.auth_client.get('/api/v1/users/', {'lastname': 'not-my-lastname'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        all_filters = {'name': 'Alex', 'lastname': 'Vellons', 'type': 'STD', 'is_verified': False}
        response = self.auth_client.get('/api/v1/users/', all_filters)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.auth_client.get('/api/v1/users/', {'search': 'vellons'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

        response = self.auth_client.get('/api/v1/users/', {'search': 'this-not-exist'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

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

        data = {'name': 'Alex', 'lastname': 'Vellons', 'type': 'BUS', 'is_verified': True, 'allow_notifications': False}
        response = self.auth_client.patch('/api/v1/users/{}/'.format(profile.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_profile = Profile.objects.all()[0]
        self.assertEqual(updated_profile.name, 'Alex')
        self.assertEqual(updated_profile.lastname, 'Vellons')
        self.assertEqual(updated_profile.type, 'STD')  # Not to update
        self.assertEqual(updated_profile.is_verified, False)  # Not to update
        self.assertEqual(updated_profile.sign_in_provider, 'password')  # Not to update
        self.assertEqual(updated_profile.fcm_token, None)
        self.assertEqual(updated_profile.allow_notifications, False)

    def test_profile_update_permission(self):
        """
        Ensure profile update view works only for the owner.
        """
        profile = Profile.objects.all()[0]

        self.auth_client2 = get_test_user_client('USER2')
        response = self.auth_client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'name': 'Alex', 'lastname': 'Vellons'}
        response = self.auth_client2.patch('/api/v1/users/{}/'.format(profile.id), data)  # USER2 try to update USER1
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
