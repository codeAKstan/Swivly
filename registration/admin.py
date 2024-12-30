from django.contrib import admin
from .models import Profile, Category, Product, ProductImage

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'photo', 'address']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'status', 'available', 'created', 'updated']
    list_filter = ['available', 'status', 'category']
    list_editable = ['price', 'available', 'status']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    actions = ['approve_products', 'reject_products']

    def approve_products(self, request, queryset):
        queryset.update(status='approved', available=True)
    approve_products.short_description = "Approve selected products"

    def reject_products(self, request, queryset):
        queryset.update(status='rejected', available=False)
    reject_products.short_description = "Reject selected products"

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']