from django import forms
from django_countries.fields import CountryField

PAYMENT_OPTIONS = (
    ('M', 'Mpesa'),
    ('P', 'Paypal')
)
class CheckoutForm(forms.Form):
    street_address = forms.CharField( widget=forms.TextInput(attrs= {'placeholder': 'lumumba drive', 'class': 'form-control'}))
    apartment = forms.CharField(widget=forms.TextInput(attrs= {'placeholder': 'apartment or suite', 'class': 'form-control'}), required=False)
    country = CountryField(blank_label='select country').formfield()
    zip = forms.CharField()
    same_billing_address = forms.BooleanField(required=False)
    save_biling_info = forms.BooleanField(required=False)
    payment_options = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPTIONS)

