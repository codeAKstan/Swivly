from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('agent', 'Agent'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    cpassword = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Role', required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=80, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']
        help_texts = {'username': None}

    def clean_cpassword(self):
        cd = self.cleaned_data
        if cd['password'] != cd['cpassword']:
            raise forms.ValidationError('Passwords must match')
        return cd['cpassword']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Save the role in the Profile model
            Profile.objects.create(user=user, role=self.cleaned_data['role'])
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']
        help_texts = {'username': None}

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role','address', 'photo']