from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from api.permissions import *
from api.serializers import *
from loopable.pagination import CustomPagination


# /users/
class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.exclude(type__in=['SYS']).prefetch_related('user').order_by('created_at')
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'lastname', 'type', 'is_verified', 'is_active']
    search_fields = ['name', 'lastname']  # ?search=LIKE in all these fields
    ordering_fields = ['name', 'lastname', 'created_at']  # ?ordering=-username


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
    

# /users/<str:pk>/rents/
class ProfileRentListAPIView(generics.ListAPIView):
    serializer_class = RentSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'product', 'status', 'payment_method']
    ordering_fields = ['created_at', 'start_time', 'end_time']
    permission_classes = [ProfileRentsIfIsOwner]

    def get_queryset(self):
        renter_id = self.kwargs['pk']
        return (Rent.objects.prefetch_related('product').prefetch_related('product__images')
                .filter(renter=renter_id).order_by('created_at'))


# /product-categories/
class ProductCategoryListAPIView(generics.ListAPIView):
    queryset = ProductCategory.objects.all().order_by('id')
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'name']
    ordering_fields = ['name']


# /products/
class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.prefetch_related('images').all().order_by('created_at')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'category', 'owner', 'active', 'stock_quantity']
    search_fields = ['name']  # ?search=LIKE in all these fields
    ordering_fields = ['name']

    def perform_create(self, serializer):
        # Get owner from the request
        serializer.save(owner=self.request.user.profile)


# /reviews/
class ProductReviewsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductReviews.objects.all().order_by('created_at')
    serializer_class = ProductReviewsSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']


# /rents/
class RentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Rent.objects.all().order_by('-start_time')
    serializer_class = RentSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'renter', 'product', 'status']
    ordering_fields = ['start_time']

    def perform_create(self, serializer):
        # Get owner from the request
        serializer.save(renter=self.request.user.profile, status='pending', payment_method='OPP')
