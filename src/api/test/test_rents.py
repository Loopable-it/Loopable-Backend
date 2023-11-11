from rest_framework import status

from api.models import Rent
from api.test.api_test_case_base import APITestCaseBase


class RentsAPITests(APITestCaseBase):

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

        response = self.auth_client.get('/api/v1/rents/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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
            'payment_method': 'PAYPAL',  # This is ignored
            'status': 'accepted',  # This is ignored
            'price': 40.00
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rent.objects.count(), 4)
        self.demo_db.r4c = Rent.objects.get(id=response.json()['id'])
        self.assertEqual(self.demo_db.r4c.payment_method, 'OPP')
        self.assertEqual(self.demo_db.r4c.price, 40)
        self.assertEqual(self.demo_db.r4c.status, 'pending')
