# Generated by Django 5.1.4 on 2025-01-01 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0013_house_location_houseimage_house_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='location',
        ),
        migrations.RemoveField(
            model_name='houseimage',
            name='house',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='House',
        ),
        migrations.DeleteModel(
            name='HouseImage',
        ),
    ]