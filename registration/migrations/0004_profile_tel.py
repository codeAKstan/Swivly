# Generated by Django 5.1.4 on 2024-12-23 09:04

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_alter_profile_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tel',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
