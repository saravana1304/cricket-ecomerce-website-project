# forms.py

from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['phone_number', 'place', 'address', 'pincode']

