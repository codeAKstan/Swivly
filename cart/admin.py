from django.contrib import admin
from .models import Configuration

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery_fee')
    list_editable = ('delivery_fee',)
    list_display_links = ('id',)
