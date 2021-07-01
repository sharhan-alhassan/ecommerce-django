
from django import forms
from django.forms.forms import Form
from django.forms.widgets import CheckboxInput, RadioSelect, TextInput

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
)


class CheckoutForm(forms.Form):
    '''
    This form is being created from the HTML fields on the bootstrap template.
    '''
    street_address = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': '1234 Main St'}
    ))
    apartment_address = forms.CharField(required=False, widget=TextInput(
        attrs={'placeholder': 'Apartment or suite'}
    ))
    country = CountryField(blank_label='select country').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100'
        })
    )
    zip = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'zip code', 
            'class': 'form-control',
        }
    ))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=RadioSelect, choices=PAYMENT_CHOICES)

