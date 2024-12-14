from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('agent', 'Agent'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
        
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    cpassword = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Role')
    

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'email'
        ]

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['cpassword']:
            raise forms.ValidationError('Password must match')
        return cd['cpassword']
