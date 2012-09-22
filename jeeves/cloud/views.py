import uuid
import core
from cloud import forms
from cloud import models
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.http import Http404


@login_required
def add(request):
    """
    Create a new cloud
    """
    message = ''
    if request.method == 'POST':
        form = forms.CloudForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.owner = request.user
            form_instance.uuid = uuid.uuid4()
            form_instance.save()
            message = 'Your cloud has been created'
            form = forms.CloudForm()
            return redirect('/cloud')
    else:
        form = forms.CloudForm()

    return direct_to_template(request,
        'cloud/add.html',
        {
            'request': request,
            'form': form,
            'message': message
        })


@login_required
def edit(request, uuid):
    """
    Edit preferences in a Cloud
    """
    cloud = models.Cloud.objects.get(uuid=uuid)

    if request.method == 'POST':
        form = forms.CloudForm(request.POST, instance=cloud)
        if form.is_valid():
            form.save()

            return redirect('/cloud/%s' % uuid)
    else:
        form = forms.CloudForm(instance=cloud)

    return direct_to_template(request,
        'cloud/cloud_edit.html',
        {
            'request': request,
            'form': form,
            'cloud': cloud
        })


@login_required
def index(request, uuid):
    """
    The overview of a single cloud
    """
    try:
        cloud = models.Cloud.objects.get(uuid=uuid)
    except models.Cloud.DoesNotExist:
        raise Http404

    return direct_to_template(request,
        'cloud/cloud_index.html',
        {
            'request': request,
            'cloud': cloud
        })


@login_required
def list(request):
    """
    Show the clouds registered for the authenticated user
    """
    return direct_to_template(request,
        'cloud/list.html',
        {
            'request': request,
            'clouds': core.models.Account.clouds(request.user)
        })


@login_required
def security_group_list(request, uuid):
    """
    List all security groups
    """
    try:
        cloud = models.Cloud.objects.get(uuid=uuid)
    except models.Cloud.DoesNotExist:
        raise Http404
    return direct_to_template(request,
        'cloud/security_group.html',
        {
            'request': request,
            'cloud': cloud,
            'security_groups': models.SecurityGroup.objects.filter(
                                cloud__uuid=uuid)
        })


@login_required
def security_group_add(request, uuid):
    """
    Add new security groups
    """
    try:
        cloud = models.Cloud.objects.get(uuid=uuid)
    except models.Cloud.DoesNotExist:
        raise Http404

    message = ''

    if request.method == 'POST':
        form = forms.SecurityGroupForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.cloud = models.Cloud.objects.get(uuid=uuid)
            form_instance.save()

            security_group = models.SecurityGroup.objects.get(id=form_instance.id)
            security_group.add_to_aws()

            message = 'Your security group has been created'
            form = forms.CloudForm()
            return redirect('/cloud/%s/security_group' % uuid)
    else:
        form = forms.SecurityGroupForm()

    return direct_to_template(request,
        'cloud/security_group_add.html',
        {
            'request': request,
            'cloud': cloud,
            'form': form,
            'message': message
        })
