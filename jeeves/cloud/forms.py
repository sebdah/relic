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


class AutoScalingGroupDefinitionForm(forms.ModelForm):
    def __init__(self, lc_choices, lb_choices, *args, **kwargs):
        super(AutoScalingGroupDefinitionForm, self).__init__(*args, **kwargs)
        self.fields['launch_config_name'] = forms.ChoiceField(
            choices=lc_choices)
        self.fields['load_balancer'] = forms.ChoiceField(choices=lb_choices)

    class Meta:
        model = models.AutoScalingGroupDefinition
        exclude = ('cluster', 'created',)


class AutoScalingGroupForm(forms.Form):
    def __init__(self, launch_configs, *args, **kwargs):
        super(AutoScalingGroupForm, self).__init__(*args, **kwargs)
        self.fields['launch_config_name'].choices = launch_configs

    name = forms.CharField(required=True, max_length=30)
    availability_zones = forms.MultipleChoiceField(required=True,
        choices=definitions.AVAILABILITY_ZONES)
    launch_config_name = forms.ChoiceField(required=True)
    min_size = forms.IntegerField(required=True, initial=1)
    max_size = forms.IntegerField(required=True, initial=1)


class LaunchConfigForm(forms.Form):
    def __init__(self, sg_choices, key_pairs, *args, **kwargs):
        super(LaunchConfigForm, self).__init__(*args, **kwargs)
        self.fields['key_name'].choices = key_pairs
        self.fields['security_groups'].choices = sg_choices

    name = forms.CharField(required=True, max_length=30)
    image_id = forms.CharField(required=True, min_length=12, max_length=12)
    key_name = forms.ChoiceField(required=True)
    user_data = forms.CharField(widget=forms.Textarea, required=False)
    security_groups = forms.MultipleChoiceField(required=True)
    instance_type = forms.ChoiceField(required=True,
        choices=definitions.INSTANCE_TYPES)
