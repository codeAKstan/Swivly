from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'paid','created', 'updated')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'price')