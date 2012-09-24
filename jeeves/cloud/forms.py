from django import forms
from cloud import models, definitions


class CloudForm(forms.ModelForm):
    class Meta:
        model = models.Cloud
        fields = ('name', 'aws_access_key', 'aws_secret_key', 'region')


class ClusterForm(forms.ModelForm):
    class Meta:
        model = models.Cluster
        exclude = ('cloud',)


class LaunchConfigForm(forms.Form):
    def __init__(self, sg_choices, *args, **kwargs):
        super(LaunchConfigForm, self).__init__(*args, **kwargs)
        self.fields['security_groups'] =\
            forms.MultipleChoiceField(required=True, choices=sg_choices)

    name = forms.CharField(required=True, max_length=30)
    image_id = forms.CharField(required=True, min_length=12, max_length=12)
    key_name = forms.CharField(required=True, max_length=30)
    user_data = forms.CharField(widget=forms.Textarea)
    instance_type = forms.ChoiceField(required=True,
        choices=definitions.INSTANCE_TYPES)
