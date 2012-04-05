from django.forms import ModelForm
from django.forms import widgets
from core import models

class AccountForm(ModelForm):
    class Meta:
        model = models.Account
        fields = ('email', 'password', 'first_name', 'last_name')
        widgets = {
            'password': widgets.PasswordInput,
        }

class AuthenticationForm(ModelForm):
    class Meta:
        model = models.Account
        fields = ('email', 'password')
        widgets = {
            'password': widgets.PasswordInput,
        }