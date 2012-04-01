from django.forms import ModelForm
from django.forms import widgets
from cloud import models

class CloudForm(ModelForm):
    class Meta:
        model = models.Cloud
        fields = ('name', 'aws_id', 'aws_secret')

class RoleForm(ModelForm):
    class Meta:
        model = models.Role
        fields = ('name', 'cloud')

class InstanceForm(ModelForm):
    class Meta:
        model = models.Instance
        fields = ('role', 'hostname', 'instance_type', 'availability_zone')

class Package(ModelForm):
    class Meta:
        model = models.Package
        field = ('name', 'role')

class EBSVolume(ModelForm):
    class Meta:
        model = models.EBSVolume
        fields = ('mountpoint', 'size', 'role')

class ElasticIP(ModelForm):
    class Meta:
        model = models.ElasticIP
        fields = ('dns_name', 'role')
