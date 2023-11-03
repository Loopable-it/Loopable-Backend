import os

import requests
from django.conf import settings
from rest_framework.test import APIClient

from api.models import Profile


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FirebaseTestUsers(metaclass=Singleton):

    def __init__(self):
        self.users = {}

    @staticmethod
    def get_jwt_token(email: str, password: str) -> str:
        url = f'{settings.FIREBASE_USER_VERIFY_SERVICE}?key={settings.FIREBASE_API_KEY}'
        data = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        print(f'Logging user {email}')
        result = requests.post(url, json=data, timeout=5)
        if result.status_code != 200:
            print(result.json())
        assert result.status_code == 200, f'status_code is: {result.status_code}'
        json_result = result.json()
        jwt = json_result.get('idToken', 'no-token')
        assert jwt[:2] == 'ey', f'jwt is: {jwt}'
        return jwt

    def get_test_user_jwt(self, username: str = 'USER1') -> str:
        email = os.getenv(f'FIREBASE_TEST_{username}_EMAIL', None)
        password = os.getenv(f'FIREBASE_TEST_{username}_PWD', None)
        assert email is not None, f'email is: {email}'
        assert password is not None
        return self.get_jwt_token(email, password)

    def get_test_user_client(self, username) -> APIClient:
        if username not in self.users:
            jwt = self.get_test_user_jwt(username)
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION=jwt)
            self.users[username] = client
        return self.users[username]

    @staticmethod
    def get_profile(username: str = 'USER1') -> Profile:
        email = os.getenv(f'FIREBASE_TEST_{username}_EMAIL', None)
        return Profile.objects.get(user__email=email)
