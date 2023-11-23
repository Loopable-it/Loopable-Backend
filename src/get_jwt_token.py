import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Take environment variables from .env file.

# https://firebase.google.com/docs/reference/rest/auth#section-sign-in-email-password
FIREBASE_USER_VERIFY_SERVICE = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword'
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY', None)  # Project settings > General > API web key


def user_login(email, password):
    url = f'{FIREBASE_USER_VERIFY_SERVICE}?key={FIREBASE_API_KEY}'
    data = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    result = requests.post(url, json=data, timeout=5)
    json_result = result.json()
    return json_result


if __name__ == '__main__':
    #input_email = os.getenv('FIREBASE_LOGIN_EMAIL', None)
    input_email = 'test_backend_2@loopable.it' # Force email
    input_password = os.getenv('FIREBASE_LOGIN_PWD', None)
    if not input_email:
        input_email = input('Email> ')
    if not input_password:
        input_password = input('Password> ')

    r = user_login(input_email, input_password)
    print(r)
    print()
    print(f'localId: {r["localId"]}\n')
    print(f'refreshToken: {r["refreshToken"]}\n')
    print(f'idToken: {r["idToken"]}')

    """
    Now you cat make http request with 'Authorization' header that contains idToken
    curl --location --request GET 'http://localhost:8000/api/v1/product-categories/' \
        --header 'Authorization: eyJhbGZ......'
    """
