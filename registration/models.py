from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Profile(models.Model):
        ROLE_CHOICES = [
        ('agent', 'Agent'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]

        user = models.OneToOneField(User, on_delete=models.CASCADE)
        role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')
        photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
        address = models.CharField(max_length=200, null=True)
        tel = PhoneNumberField(null=True, blank=True)

        def __str__(self):
            return f'{self.user.username} Profile'

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('pending', 'Pending'), ('expired', 'Expired')])

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('pending', 'Pending'), ('failed', 'Failed')])


