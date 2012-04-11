from django.forms import ModelForm
from django.forms import widgets
from cloud import models

class CloudForm(ModelForm):
    class Meta:
        model = models.Cloud
        fields = ('name', 'aws_id', 'aws_secret', 'aws_key_pair')

class RoleForm(ModelForm):
    class Meta:
        model = models.Role
        fields = ('name',)

class RoleRelationForm(ModelForm):
    class Meta:
        model = models.RoleRelation
        fields = ('role',)

class InstanceForm(ModelForm):
    class Meta:
        model = models.Instance
        fields = ('hostname', 'instance_type', 'availability_zone')

class PackageForm(ModelForm):
    class Meta:
        model = models.Package
        field = ('name', 'role')

class EBSVolumeForm(ModelForm):
    class Meta:
        model = models.EBSVolume
        fields = ('mountpoint', 'size',)

class ElasticIPForm(ModelForm):
    class Meta:
        model = models.ElasticIP
        fields = ('dns_name',)
