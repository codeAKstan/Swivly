# Generated by Django 5.1.4 on 2024-12-28 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_remove_product_image_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]