from rest_framework import status

from api.models import Profile
from api.test.api_test_case_base import APITestCaseBase


class UsersAPITests(APITestCaseBase):

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
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(f'/api/v1/users/{self.demo_db.profile1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(f'/api/v1/users/{self.demo_db.profile1.id}/', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_list(self):
        """
        Ensure profile list view works.
        """
        profile = Profile.objects.get(id=self.demo_db.profile1.id)

        response = self.auth_client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

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
        Same user can see all fields, other users can see only public fields.
        """
        response = self.auth_client.get(f'/api/v1/users/{self.demo_db.profile1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'email', status_code=200)
        self.assertContains(response, 'name', status_code=200)
        self.assertContains(response, 'lastname', status_code=200)
        self.assertContains(response, 'type', status_code=200)
        self.assertContains(response, 'is_verified', status_code=200)
        self.assertContains(response, 'is_active', status_code=200)
        self.assertContains(response, 'sign_in_provider', status_code=200)
        self.assertContains(response, 'is_complete', status_code=200)
        self.assertContains(response, 'image', status_code=200)
        self.assertContains(response, 'fcm_token', status_code=200)
        self.assertContains(response, 'allow_notifications', status_code=200)

        response = self.auth_client2.get(f'/api/v1/users/{self.demo_db.profile1.id}/')  # USER2 try get USER1
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'email', status_code=200)
        self.assertContains(response, 'name', status_code=200)
        self.assertContains(response, 'lastname', status_code=200)
        self.assertContains(response, 'type', status_code=200)
        self.assertContains(response, 'is_verified', status_code=200)
        self.assertContains(response, 'is_active', status_code=200)
        self.assertNotContains(response, 'sign_in_provider', status_code=200)
        self.assertNotContains(response, 'is_complete', status_code=200)
        self.assertContains(response, 'image', status_code=200)
        self.assertNotContains(response, 'fcm_token', status_code=200)
        self.assertNotContains(response, 'allow_notifications', status_code=200)

    def test_profile_update(self):
        """
        Ensure profile update view works.
        """
        data = {'name': 'Alex', 'lastname': 'Vellons', 'type': 'BUS', 'is_verified': True, 'allow_notifications': False}
        response = self.auth_client.patch(f'/api/v1/users/{self.demo_db.profile1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_profile = Profile.objects.get(id=self.demo_db.profile1.id)
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
        response = self.auth_client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'name': 'Alex', 'lastname': 'Vellons'}
        response = self.auth_client2.patch(f'/api/v1/users/{self.demo_db.profile1.id}/', data)  # USER2 try update USER1
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
