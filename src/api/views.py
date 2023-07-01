from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from api.permissions import *
from api.serializers import *


# /users/
class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.exclude(type__in=['SYS']).order_by('created_at')
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'lastname', 'type', 'is_verified']
    search_fields = ['name', 'lastname']  # ?search=LIKE in all these fields
    ordering_fields = ['name', 'lastname']  # ?ordering=-username


# /users/<str:pk>/ (only owner of account can update)
class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    http_method_names = ['get', 'patch', 'options']
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [ProfileEditIfIsOwner]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ProfileSerializerUpdate
        return ProfileSerializer
