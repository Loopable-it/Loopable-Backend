from rest_framework import status
from rest_framework.exceptions import APIException


class NoAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'No authentication token provided'
    default_code = 'no_auth_token'


class InvalidAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Invalid authentication token provided'
    default_code = 'invalid_token'


class ForbiddenUser(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'User is not active. Disabled in database.'
    default_code = 'disabled_user'


class FirebaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'The user provided with the auth token is not a valid Firebase user, it has no Firebase UID'
    default_code = 'no_firebase_uid'
