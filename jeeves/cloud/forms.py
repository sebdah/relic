from django.forms import ModelForm
from django.forms import widgets
from cloud import models

class CloudForm(ModelForm):
    class Meta:
        model = models.Cloud
        fields = ('name', 'aws_id', 'aws_secret')