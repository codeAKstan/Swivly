from django import forms
from registration.models import Profile

class AddressForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'city', 'state']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }
