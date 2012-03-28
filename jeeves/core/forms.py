from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from core import models

class AccountForm(ModelForm):
	class Meta:
		model = models.Account
		fields = ('email', 'password', 'first_name', 'last_name')
		widgets = {
            'password': PasswordInput,
        }

class AuthenticationForm(ModelForm):
	class Meta:
		model = models.Account
		fields = ('email', 'password')
		widgets = {
            'password': PasswordInput,
        }