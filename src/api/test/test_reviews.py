from rest_framework import status

from api.models import ProductReviews
from api.test.api_test_case_base import APITestCaseBase


class ReviewsAPITest(APITestCaseBase):
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
        response = self.client.post('/api/v1/reviews/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(f'/api/v1/products/{self.demo_db.p1.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(f'/api/v1/users/{self.demo_db.profile1.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reviews_list(self):
        """
        Ensure reviews list view works.
        """
        response = self.auth_client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.auth_client.get('/api/v1/products/1234/reviews/')  # fake id
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.auth_client.get(f'/api/v1/products/{self.demo_db.p1.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

        response = self.auth_client2.get(f'/api/v1/products/{self.demo_db.p1.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

        # Test filters
        response = self.auth_client.get(f'/api/v1/products/{self.demo_db.p1.id}/reviews/',
                                        {'created_by': self.demo_db.profile1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

        response = self.auth_client.get(f'/api/v1/products/{self.demo_db.p1.id}/reviews/',
                                        {'rating': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_reviews_create(self):
        """
        Ensure reviews create view works.
        """
        response = self.auth_client.post('/api/v1/reviews/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'product': self.demo_db.p4.id,
            'rating': 5,
            'content': 'Test review',
            'created_by': self.demo_db.profile1.id
        }
        response = self.auth_client.post('/api/v1/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data = {
            'product': self.demo_db.p3.id,
            'rating': 5,
            'content': 'Test review',
            'created_by': self.demo_db.profile1.id
        }
        response = self.auth_client.post('/api/v1/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductReviews.objects.count(), 5)
        product_review = ProductReviews.objects.get(id=response.json()['id'])
        self.assertEqual(product_review.product_id, self.demo_db.p3.id)
        self.assertEqual(product_review.rating, data['rating'])
        self.assertEqual(product_review.content, data['content'])
        self.assertEqual(product_review.created_by_id, self.demo_db.profile1.id)

    def test_users_reviews_list(self):
        """
        Ensure users reviews list view works.
        """
        response = self.auth_client.get('/api/v1/users/1234/reviews/')  # fake id
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.auth_client.get(f'/api/v1/users/{self.demo_db.profile1.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

        # Test filters
        response = self.auth_client.get(f'/api/v1/users/{self.demo_db.profile1.id}/reviews/',
                                        {'product': self.demo_db.p1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

        response = self.auth_client.get(f'/api/v1/users/{self.demo_db.profile1.id}/reviews/',
                                        {'rating': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)
