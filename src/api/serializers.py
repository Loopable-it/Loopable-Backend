from rest_framework import serializers

from api.models import Profile, ProductCategory, ProductImage, Product, ProductReviews, Rent


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'email', 'name', 'lastname', 'type', 'is_verified', 'is_active', 'image')


class ProfileSerializerUpdate(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    """
    This serializer show personal information of a user.
    """

    class Meta:
        model = Profile
        read_only_fields = ('id', 'user', 'type', 'is_verified', 'sign_in_provider', 'created_at', 'updated_at')
        exclude = ('user',)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')

    @staticmethod
    def get_images(obj):
        return ProductImageSerializer(obj.images.all(), many=True).data


class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviews
        fields = '__all__'


class RentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'
        read_only_fields = ('id', 'renter', 'status', 'payment_method', 'created_at', 'updated_at')


class RentSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Rent
        fields = '__all__'
        read_only_fields = ('id', 'renter', 'created_at', 'updated_at')
