from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms.widgets import PasswordInput,TextInput

# creating user we use this form 
class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):

        # Set placeholders
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'

        # Hide last_login field
        if 'last_login' in self.fields:
            self.fields['last_login'].widget = forms.HiddenInput()
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']
# user athendication for we using this form 
      


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

    


