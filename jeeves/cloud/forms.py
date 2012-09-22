from django.forms import ModelForm
from cloud import models


class CloudForm(ModelForm):
    class Meta:
        model = models.Cloud
        fields = ('name', 'aws_id', 'aws_secret', 'region')


class SecurityGroupForm(ModelForm):
    class Meta:
        model = models.SecurityGroup
        fields = ('name', 'description')
