from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator

from django.core.validators import RegexValidator

numeric = RegexValidator(r'^[0-9+]', 'Solo caracteres numericos.')

class BasicForm(forms.Form):
    user = forms.CharField(
        widget     = forms.TextInput(),
        validators = [MinLengthValidator(4), MaxLengthValidator(16), numeric]
    )
    password = forms.CharField(
        widget     = forms.TextInput(attrs={'type':'password'}),
        validators = [MinLengthValidator(4), MaxLengthValidator(16)]
    )
