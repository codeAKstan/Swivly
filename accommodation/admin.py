from django.contrib import admin
from .models import Location, House, HouseImage
# Register your models here.

class HouseImageInline(admin.TabularInline):
    model = HouseImage
    extra = 1


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['lodge_name', 'location', 'price', 'number_of_rooms', 'is_available','status', 'created']
    list_filter = ['is_available', 'location']
    list_editable = ['is_available', 'status']
    search_fields = ['lodge_name', 'description']
    inlines = [HouseImageInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state']
    search_fields = ['name', 'city', 'state']