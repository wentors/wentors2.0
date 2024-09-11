from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
# from crispy_bootstrap5.bootstrap5 import FloatingField

class SubscriptionForm(forms.Form):
    fullname = forms.CharField(label="Full Name", max_length=50, help_text='required')
    email = forms.EmailField(label="Email", help_text='required')
    country = forms.CharField(label="Country", max_length=50, help_text='required')
    phonenumber = forms.CharField(label="Phone Number", help_text='required')
    countrycode = forms.CharField(label="Country Code", max_length=5, help_text='required')
    payment_method = forms.CharField(label="stripe/paystack", max_length=20)
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].widget = forms.TextInput(attrs={
            'id': 'fullname',
            'class': 'form-control',
            'placeholder': 'Jane Buttons'})
        self.fields['email'].widget = forms.EmailInput(attrs={
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'email@mailserver.com'})
        self.fields['country'].widget = forms.TextInput(attrs={
            'id': 'country',
            'class': 'form-control',
            'placeholder': 'Country'})
        self.fields['phonenumber'].widget = forms.TextInput(attrs={
            'id': 'phonenumber',
            'class': 'form-control',
            'placeholder': '0000 000 0000'})
        self.fields['countrycode'].widget = forms.TextInput(attrs={
            'id': 'countrycode',
            'class': 'form-control',
            'placeholder': '+000'})
        self.fields['payment_method'].widget = forms.HiddenInput(attrs={
            'id': 'payment_method'
        })
