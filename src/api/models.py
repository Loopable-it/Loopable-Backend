import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

PROFILE_TYPE_CHOICES = [
    ('STD', 'Standard'),
    ('BUS', 'Business'),
    ('SYS', 'System')
]

PAYMENT_METHOD_CHOICES = [
    ('OPP', 'OnPlacePayment'),
    ('CARD', 'Card'),
    ('PAYPAL', 'PayPal'),
    ('BANK', 'BankTransfer')
]

RENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('canceled', 'Canceled'),
]


class Profile(models.Model):
    id = models.CharField(max_length=32, primary_key=True, unique=True)  # Firebase UID
    user = models.OneToOneField(get_user_model(), on_delete=models.PROTECT, related_name='profile')
    name = models.CharField(max_length=32, null=True)
    lastname = models.CharField(max_length=32, null=True)
    type = models.CharField(max_length=3, choices=PROFILE_TYPE_CHOICES, default='STD')
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sign_in_provider = models.CharField(max_length=32)
    province = models.CharField(max_length=64, null=True)
    is_complete = models.BooleanField(default=False)
    image = models.CharField(max_length=1024, null=True)
    fcm_token = models.CharField(max_length=256, null=True)  # Firebase Cloud Messaging Token
    allow_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<Profile {self.id} {self.lastname} {self.name}>'

    def __str__(self):
        return f'@{self.id}'


@receiver(post_save, sender=get_user_model())  # Received from firebase_auth
def create_user_profile(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    if created:
        Profile.objects.create(id=instance.username, user=instance)


class ProductCategory(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=512, null=True)

    class Meta:
        verbose_name_plural = 'Product categories'

    def __repr__(self):
        return f'<Category {self.name}>'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    owner = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products_list')
    stock_quantity = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)
    latitude = models.FloatField()  # TODOOO: use PostGIS
    longitude = models.FloatField()  # TODOOO: use PostGIS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<Product {self.id} {self.name}>'

    def __str__(self):
        return f'{self.name}'


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f'<ProductImage {self.id} {self.image}>'

    def __str__(self):
        return f'{self.image}'


class ProductReviews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    owner = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='reviews')
    content = models.TextField(max_length=4096)
    rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product reviews'

    def __repr__(self):
        return f'<ProductReviews {self.id} {self.content}>'

    def __str__(self):
        return f'{self.content}'


class Rent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHOD_CHOICES, default='OPP')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    renter = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='rents')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_rents')
    status = models.CharField(max_length=8, choices=RENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<Rent {self.id}>'

    def __str__(self):
        return f'{self.id}'
