# Generated by Django 4.2.6 on 2023-10-29 08:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_productreviews"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="product",
            name="latitude",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="longitude",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="stock_quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]