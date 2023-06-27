# Generated by Django 4.2.2 on 2023-06-27 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False,
                                        unique=True)),
                ('name', models.CharField(max_length=32, null=True)),
                ('lastname', models.CharField(max_length=32, null=True)),
                ('type', models.CharField(choices=[('STD', 'Standard'), ('BUS', 'Business'), ('SYS', 'System')],
                                          default='STD', max_length=3)),
                ('is_verified', models.BooleanField(default=False)),
                ('sign_in_provider', models.CharField(max_length=32)),
                ('fcm_token', models.CharField(max_length=256, null=True)),
                ('allow_notifications', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile',
                                              to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]