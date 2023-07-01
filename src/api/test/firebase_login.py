import os

import requests
from django.conf import settings
from rest_framework.test import APIClient


def get_jwt_token(email: str, password: str) -> str:
    url = '{}?key={}'.format(settings.FIREBASE_USER_VERIFY_SERVICE, settings.FIREBASE_API_KEY)
    data = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    result = requests.post(url, json=data)
    json_result = result.json()
    return json_result.get('idToken', 'no-token')


def get_test_user_jwt(username: str = 'USER1') -> str:
    email = os.getenv('FIREBASE_TEST_{}_EMAIL'.format(username), None)
    password = os.getenv('FIREBASE_TEST_{}_PWD'.format(username), None)
    assert email is not None
    assert password is not None
    return get_jwt_token(email, password)


def get_test_user_client(username) -> APIClient:
    jwt = get_test_user_jwt(username)
    assert jwt[:2] == 'ey'
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=jwt)
    return client
