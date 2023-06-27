from rest_framework import serializers

from users.models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'lastname', 'type', 'is_verified')


class ProfileSerializerUpdate(serializers.ModelSerializer):
    """
    This serializer show personal information of a user.
    """

    class Meta:
        model = Profile
        read_only_fields = ('id', 'user', 'type', 'is_verified', 'sign_in_provider', 'created_at', 'updated_at')
        exclude = ('user',)
