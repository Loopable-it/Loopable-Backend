from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.generics import get_object_or_404

from api.models import Profile, ProductCategory, Rent, Product, ProductReviews, ProductImage
from api.permissions import ProfileEditIfIsOwner, ProfileRentsIfIsOwner, ProductEditIfIsOwner, \
    ProductImageEditIfIsOwner, ReviewsIfIsRenter
from api.serializers import ProfileSerializer, ProfileSerializerUpdate, ProductCategorySerializer, \
    ProductSerializer, RentSerializer, RentCreateSerializer, ProductReviewsSerializer, ProductImageSerializer
from loopable.pagination import CustomPagination


# /users/
class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.exclude(type__in=['SYS']).prefetch_related('user').order_by('created_at')
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'lastname', 'type', 'is_verified', 'is_active']
    search_fields = ['name', 'lastname']  # ?search=LIKE in all these fields
    ordering_fields = ['name', 'lastname', 'created_at']  # ?ordering=-lastname


# /users/<str:pk>/ (only owner of account can update)
class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    http_method_names = ['get', 'patch', 'options']
    queryset = Profile.objects.all()
    permission_classes = [ProfileEditIfIsOwner]

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            # Serializer just for swagger schema generation metadata
            if self.request.method == 'PATCH':
                return ProfileSerializerUpdate
            return ProfileSerializer
        if self.request.method == 'PATCH' or self.kwargs['pk'] == self.request.user.username:
            return ProfileSerializerUpdate
        return ProfileSerializer


# /users/<str:pk>/rents/
class ProfileRentListAPIView(generics.ListAPIView):
    serializer_class = RentSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'status', 'payment_method']
    ordering_fields = ['created_at', 'start_time', 'end_time']
    permission_classes = [ProfileRentsIfIsOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # Queryset just for swagger schema generation metadata
            return Rent.objects.none()
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
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.prefetch_related('images').all().order_by('created_at')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'category', 'owner', 'active', 'stock_quantity']
    search_fields = ['name']  # ?search=LIKE in all these fields
    ordering_fields = ['name']

    def perform_create(self, serializer):
        # Get owner from the request
        serializer.save(owner_id=self.request.user.username)


# /products/<str:pk>/ (only owner of account can update)
class ProductRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    http_method_names = ['get', 'patch', 'options']
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductEditIfIsOwner]


# /products/<str:pk>/images/ (only owner of product can create)
class ProductImageCreateAPIView(generics.CreateAPIView):
    queryset = ProductImage.objects.all().order_by('created_at')
    serializer_class = ProductImageSerializer
    permission_classes = [ProductImageEditIfIsOwner]

    def perform_create(self, serializer):
        # Get product from the request
        serializer.save(product_id=self.kwargs['pk'])


# /products/<str:pk>/images/<str:id_img>/ (only owner of product can delete)
class ProductImageDestroyAPIView(generics.DestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [ProductImageEditIfIsOwner]

    def get_object(self):
        return get_object_or_404(ProductImage, id=self.kwargs.get('id_img'))


# /reviews/
class ProductReviewsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductReviews.objects.all().order_by('created_at')
    serializer_class = ProductReviewsSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'product', 'owner']
    permission_classes = [ReviewsIfIsRenter]
    search_fields = ['content']


# /rents/
class RentCreateAPIView(generics.CreateAPIView):
    queryset = Rent.objects.all().order_by('created_at')
    serializer_class = RentCreateSerializer

    def perform_create(self, serializer):
        # Get owner from the request
        serializer.save(renter_id=self.request.user.username, status='pending', payment_method='OPP')
