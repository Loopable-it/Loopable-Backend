import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

PROFILE_TYPE_CHOICES = [
    ('STD', 'Standard'),
    ('BUS', 'Business'),
    ('SYS', 'System')
]


class Profile(models.Model):
    id = models.CharField(max_length=32, primary_key=True, unique=True)  # Firebase UID
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    name = models.CharField(max_length=32, null=True)
    lastname = models.CharField(max_length=32, null=True)
    type = models.CharField(max_length=3, choices=PROFILE_TYPE_CHOICES, default='STD')
    is_verified = models.BooleanField(default=False)
    sign_in_provider = models.CharField(max_length=32)
    province = models.CharField(max_length=64, null=True)
    is_complete = models.BooleanField(default=False)
    image = models.CharField(max_length=1024, null=True)
    fcm_token = models.CharField(max_length=256, null=True)  # Firebase Cloud Messaging Token
    allow_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '<Profile {} {} {}>'.format(self.id, self.lastname, self.name)

    def __str__(self):
        return '@{}'.format(self.id)


@receiver(post_save, sender=User)  # Received from firebase_auth
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(id=instance.username, user=instance)


class ProductCategory(models.Model):
    name = models.CharField(max_length=32, primary_key=True, unique=True)
    description = models.CharField(max_length=512, null=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    owner = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products_list')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '<Product {} {}>'.format(self.id, self.name)

    def __str__(self):
        return '{}'.format(self.name)


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return '<ProductImage {} {}>'.format(self.id, self.image)

    def __str__(self):
        return '{}'.format(self.image)