import firebase_admin
from django.contrib.auth import get_user_model
from django.utils import timezone
from firebase_admin import auth
from firebase_admin import credentials
from rest_framework import authentication

from firebase_utility.exceptions import NoAuthToken, BrokenAuthToken, InvalidAuthToken, FirebaseError, ForbiddenUser
from loopable import settings

credential = credentials.Certificate(settings.FIREBASE_CREDENTIAL)
default_app = firebase_admin.initialize_app(credential)


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise NoAuthToken()

        id_token = auth_header.split(' ').pop()
        try:
            decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=20)
        except Exception as e:  # pylint: disable=broad-except
            if str(e).startswith('Token used too early'):
                print(f'warning: {e}')
            raise BrokenAuthToken() from e

        if not id_token or not decoded_token:
            raise InvalidAuthToken()
        # print('decoded_token {}'.format(decoded_token))

        try:
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            sign_in_provider = decoded_token.get('firebase')['sign_in_provider']
        except Exception as e:
            raise FirebaseError() from e

        user, created = get_user_model().objects.select_related('profile').get_or_create(username=uid)
        if not user.is_active:
            raise ForbiddenUser()

        # Update last login every 30 minutes
        if user.last_login and user.last_login < timezone.now() - timezone.timedelta(minutes=30) or user.email != email:
            get_user_model().objects.filter(username=uid).update(last_login=timezone.localtime(), email=email)

        if created:
            user.profile.sign_in_provider = sign_in_provider
            user.profile.save()
        elif user.profile.sign_in_provider != sign_in_provider:  # Update sign_in_provider if changed
            user.profile.sign_in_provider = sign_in_provider
            user.profile.save()

        return user, created
