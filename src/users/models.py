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
