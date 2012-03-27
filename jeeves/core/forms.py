from django.forms import ModelForm
from core import models

class AccountForm(ModelForm):
	class Meta:
		model = models.Account