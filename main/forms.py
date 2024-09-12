from django import forms
from django.core.exceptions import ValidationError
import re


class SubscriptionForm(forms.Form):
    fullname = forms.CharField(label="Full Name", max_length=50, required=True, help_text='Enter full name')
    email = forms.EmailField(label="Email", required=True, help_text='Enter email')
    country = forms.CharField(label="Country", required=True, max_length=50, help_text='Enter country')
    phonenumber = forms.CharField(label="Phone Number", max_length=18, min_length=4, required=True, help_text='Enter phone number')
    countrycode = forms.CharField(label="Country Code", required=True, max_length=4, )
    payment_method = forms.CharField(label="stripe/paystack", required=True, max_length=20)

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].widget = forms.TextInput(attrs={
            'id': 'fullname',
            'class': 'form-control',
            'placeholder': 'Jane Buttons',
            })
        self.fields['email'].widget = forms.EmailInput(attrs={
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'email@mailserver.com',
            })
        self.fields['country'].widget = forms.TextInput(attrs={
            'id': 'country',
            'class': 'form-control',
            'placeholder': 'Country',
            })
        self.fields['phonenumber'].widget = forms.TextInput(attrs={
            'id': 'phonenumber',
            'class': 'form-control',
            'placeholder': '0000 000 0000',
            })
        self.fields['countrycode'].widget = forms.TextInput(attrs={
            'id': 'countrycode',
            'class': 'form-control',
            'placeholder': '+000',
            })
        self.fields['payment_method'].widget = forms.HiddenInput(attrs={
            'id': 'payment_method',
        })


    def clean_payment_method(self):
        data = self.cleaned_data["payment_method"]
        if data not in ("paystack", "stripe",):
            raise ValidationError("Invalid payment method")
        return data

    def clean_phonenumber(self):
        data = self.cleaned_data['phonenumber']
        if not data.isdigit():
            raise ValidationError("Phone number should only contain numbers")
        return data

    def clean_countrycode(self):
        data = self.cleaned_data['countrycode']
        if not re.match("^\+?\d{1,3}$", data):
            raise ValidationError("Country code: 1 to 3 digits, can begin with '+'")
        return data
