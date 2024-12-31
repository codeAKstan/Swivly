from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from django.utils.text import slugify

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
        city = models.CharField(max_length=100, blank=True)
        state = models.CharField(max_length=100, blank=True)
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
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
    decimal_places=2)
    available = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 
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
        if not self.slug:
            raise ValueError("Slug is missing for product: {}".format(self.name))
        return reverse('registration:product_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug if it's empty
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/%Y/%m/%d')

    def __str__(self):
        return f"Image for {self.product.name}"


class Location(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class House(models.Model):
    location = models.ForeignKey(Location, related_name='houses', on_delete=models.CASCADE)
    lodge_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_rooms = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='houses/%Y/%m/%d', blank=True)
    video = models.FileField(upload_to='houses/videos/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lodge_name

class HouseImage(models.Model):
    house = models.ForeignKey(House, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='houses/images/%Y/%m/%d')

    def __str__(self):
        return f"Image for {self.house.title}"