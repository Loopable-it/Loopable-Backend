from rest_framework import serializers

from api.models import Profile, ProductCategory, ProductImage, Product, ProductReviews, Rent


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'email', 'name', 'lastname', 'type', 'is_verified', 'is_active', 'image')


class ProfileSerializerUpdate(serializers.ModelSerializer):
    """
    This serializer show personal information of a user.
    """
    email = serializers.EmailField(source='user.email', read_only=True)
    created_at = CustomDateTimeField(read_only=True)
    updated_at = CustomDateTimeField(read_only=True)

    class Meta:
        model = Profile
        read_only_fields = ('id', 'user', 'type', 'is_verified', 'sign_in_provider', 'created_at', 'updated_at')
        exclude = ('user',)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(read_only=True)

    class Meta:
        model = ProductImage
        fields = '__all__'
        read_only_fields = ('product',)


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    created_at = CustomDateTimeField(read_only=True)
    updated_at = CustomDateTimeField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

    @staticmethod
    def get_images(obj):
        return ProductImageSerializer(obj.images.all(), many=True).data


class ProductReviewsSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(read_only=True)

    class Meta:
        model = ProductReviews
        fields = '__all__'


class RentCreateSerializer(serializers.ModelSerializer):
    created_at = CustomDateTimeField(read_only=True)
    updated_at = CustomDateTimeField(read_only=True)

    class Meta:
        model = Rent
        fields = '__all__'
        read_only_fields = ('id', 'renter', 'status', 'payment_method', 'created_at', 'updated_at')


class RentSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    created_at = CustomDateTimeField(read_only=True)
    updated_at = CustomDateTimeField(read_only=True)
    start_time = CustomDateTimeField(read_only=True)
    end_time = CustomDateTimeField(read_only=True)

    class Meta:
        model = Rent
        fields = '__all__'
        read_only_fields = ('id', 'renter', 'created_at', 'updated_at')


class RentStatusSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    created_at = CustomDateTimeField(read_only=True)
    updated_at = CustomDateTimeField(read_only=True)
    start_time = CustomDateTimeField(read_only=True)
    end_time = CustomDateTimeField(read_only=True)

    class Meta:
        model = Rent
        fields = '__all__'
        read_only_fields = (
            'id', 'product', 'renter', 'price', 'start_time', 'end_time', 'payment_method', 'created_at', 'updated_at'
            )
