from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse

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


# for categories and products
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('registration:product_list_by_category',
        args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
    decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('registration:product_detail',
                       args=[self.id, self.slug])