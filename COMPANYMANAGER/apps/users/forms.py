from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields =[
            'username',
            'email',
            'password1',
            'password2',
        ]

#modelform allows us to work with a specific database modelform

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    #allow user to change username and email in profile page
    class Meta:
        model = User
        fields =[
            'username',
            'email',
            'first_name',
            'last_name'
        ]

class ProfileUpdateForm(forms.ModelForm):
    #update image in profile
    class Meta:
        model = Profile
        fields = ['image']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['position']