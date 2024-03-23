from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
import re
from .models import UserProfile
from django.core.validators import RegexValidator
from django import forms
from django.contrib.auth import authenticate

# creating user we use this form 
class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        # Set placeholders
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields['place'].widget.attrs['placeholder'] = 'Enter your place'

        # Hide last_login field
        if 'last_login' in self.fields:
            self.fields['last_login'].widget = forms.HiddenInput()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','phone_number', 'place']

    phone_number = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits')])
    place = forms.CharField(max_length=255)

    # Form validation for username
    def clean_username(self):   
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        if not username:
            raise forms.ValidationError('Username is required')

        # Check for spaces in the username
        if ' ' in username:
            raise forms.ValidationError('Spaces are not allowed in the username')

        # Check for special characters in the username
        if not username.isalnum():
            raise forms.ValidationError('Special characters are not allowed in the username')

        # Check for numbers in the username
        if any(char.isdigit() for char in username):
            raise forms.ValidationError('Numbers are not allowed in the username')
        return username
    
        
    # Form validation for email
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if email is empty
        if not email:
            raise forms.ValidationError('Email is required for account creation')

        # Check if '@' is present in the email
        if '@' not in email:
            raise forms.ValidationError('Invalid email format. "@" is required.')
        
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not email:
            raise forms.ValidationError('Email is required')

        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered')
        return email
    
    # Custom password validator
    def validate_password(self, password):
        if len(password) < 8:
            raise forms.ValidationError('Password should be at least 8 characters long')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError('Password should include at least one special character')

    # Form validation for password1 and password2
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        self.validate_password(password1)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        self.validate_password(password2)
        return password2
    
    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        phone_number = cleaned_data.get('phone_number')

        # Check if the phone number is unique
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', 'This phone number is already exists')

        return cleaned_data
    
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.save()

        # Create UserProfile with additional fields
        UserProfile.objects.create(
            user=user,
            phone_number=self.cleaned_data['phone_number'],
            place=self.cleaned_data['place'],
        )

        return user




