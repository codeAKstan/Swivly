from django import forms
from .models import House, HouseImage


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['location', 'lodge_name', 'description', 'price', 'number_of_rooms', 'image', 'video']

class HouseImageForm(forms.ModelForm):
    class Meta:
        model = HouseImage
        fields = ['image']