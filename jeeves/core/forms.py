from django import forms
from core import models

class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')
        widgets = {
            'password': forms.widgets.PasswordInput,
        }
    
    confirm_password = forms.CharField(widget = forms.PasswordInput())

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.widgets.PasswordInput,
        }

class AuthenticationForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('email', 'password')
        widgets = {
            'password': forms.widgets.PasswordInput,
        }

class LostPasswordForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ('email',)
