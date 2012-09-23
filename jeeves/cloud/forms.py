from django.forms import ModelForm
from cloud import models


class CloudForm(ModelForm):
    class Meta:
        model = models.Cloud
        fields = ('name', 'aws_access_key', 'aws_secret_key', 'region')


class ClusterForm(ModelForm):
    class Meta:
        model = models.Cluster
        exclude = ('cloud',)
