# Generated by Django 4.2.2 on 2023-06-30 20:32

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
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=2048)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False,
                                           verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('description', models.CharField(max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=32, null=True)),
                ('lastname', models.CharField(max_length=32, null=True)),
                ('type', models.CharField(choices=[('STD', 'Standard'), ('BUS', 'Business'), ('SYS', 'System')],
                                          default='STD', max_length=3)),
                ('is_verified', models.BooleanField(default=False)),
                ('sign_in_provider', models.CharField(max_length=32)),
                ('province', models.CharField(max_length=64, null=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('image', models.CharField(max_length=1024, null=True)),
                ('fcm_token', models.CharField(max_length=256, null=True)),
                ('allow_notifications', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile',
                                              to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images',
                                              to='api.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products_list',
                                    to='api.productcategory'),  # noqa
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products',
                                    to='api.profile'),
        ),
    ]
