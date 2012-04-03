import uuid
import core
from cloud import forms
from cloud import models
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail, create_update
from django.contrib import auth
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
            form_instance = form.save(commit = False)
            form_instance.owner = request.user
            form_instance.uuid = uuid.uuid4()
            form_instance.save()
            message = 'Your cloud has been created'
            form = forms.CloudForm()
            return redirect('/cloud')
    else:
        form = forms.CloudForm()

    return direct_to_template(  request,
                                'cloud/add.html',
                                {'request': request,
                                'form': form,
                                'message': message, })

@login_required
def index(request, uuid, role_id = None):
    """
    The overview of a single cloud
    """
    try:
        cloud = models.Cloud.objects.get(uuid = uuid)
    except models.Cloud.DoesNotExist:
        raise Http404

    return direct_to_template(  request,
                                'cloud/index.html',
                                {'request': request,
                                'cloud': models.Cloud.objects.get(uuid = uuid)})

@login_required
def instance_add(request, uuid, role_id):
    """
    Add a new instance to the cloud
    """
    message = ''
    if request.method == 'POST':
        form = forms.InstanceForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit = False)
            form_instance.cloud = models.Cloud.objects.get(uuid = uuid)
            form_instance.role = models.Role.objects.get(id = role_id)
            form_instance.save()
            message = 'Your instance has been added'
            return redirect('/cloud/%s' % uuid)
    else:
        form = forms.InstanceForm()

    return direct_to_template(  request,
                                'cloud/instance_add.html',
                                {'request': request,
                                'form': form,
                                'cloud': models.Cloud.objects.get(uuid = uuid),
                                'message': message, })

@login_required
def instance_edit(request, uuid, role_id, instance_id):
    """
    Add a new Instance to the Cloud
    """
    message = ''
    if request.method == 'POST':
        form = forms.InstanceForm(  request.POST, 
                                    instance = models.Instance.objects.get(id = instance_id))
        if form.is_valid():
            form_instance = form.save(commit = False)
            form_instance.cloud = models.Cloud.objects.get(uuid = uuid)
            form_instance.role = models.Role.objects.get(id = role_id)
            form_instance.save()
            message = 'Your instance has been added'
            return redirect('/cloud/%s' % uuid)
    else:
        form = forms.InstanceForm(instance = models.Instance.objects.get(id = instance_id))

    return direct_to_template(  request,
                                'cloud/instance_edit.html',
                                {'request': request,
                                'form': form,
                                'cloud': models.Cloud.objects.get(uuid = uuid),
                                'role_id': role_id,
                                'instance': models.Instance.objects.get(id = instance_id),
                                'message': message, })

@login_required
def instance_edit_ebs(request, uuid, role_id, instance_id):
    """
    Add a new EBSVolume to the Instance
    """
    message = ''
    if request.method == 'POST':
        form = forms.EBSVolumeForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit = False)
            form_instance.cloud = models.Cloud.objects.get(uuid = uuid)
            form_instance.instance = models.Instance.objects.get(id = instance_id)
            form_instance.save()
            
            message = 'Your EBS has been added'
            form = forms.EBSVolumeForm()
    else:
        form = forms.EBSVolumeForm()

    return direct_to_template(  request,
                                'cloud/instance_edit_ebs.html',
                                {'request': request,
                                'form': form,
                                'cloud': models.Cloud.objects.get(uuid = uuid),
                                'role_id': role_id,
                                'instance': models.Instance.objects.get(id = instance_id),
                                'message': message, })

@login_required
def instance_edit_elastic_ip(request, uuid, role_id, instance_id):
    """
    Add a new Elastic IP to the Instance
    """
    message = ''
    if request.method == 'POST':
        form = forms.ElasticIPForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit = False)
            form_instance.cloud = models.Cloud.objects.get(uuid = uuid)
            form_instance.instance = models.Instance.objects.get(id = instance_id)
            form_instance.save()

            message = 'Your Elastic IP has been added'
            form = forms.ElasticIPForm()
    else:
        form = forms.ElasticIPForm()

    return direct_to_template(  request,
                                'cloud/instance_edit_elastic_ip.html',
                                {'request': request,
                                'form': form,
                                'cloud': models.Cloud.objects.get(uuid = uuid),
                                'role_id': role_id,
                                'instance': models.Instance.objects.get(id = instance_id),
                                'message': message, })

@login_required
def instance_delete(request, uuid, role_id, instance_id):
    """
    Delete an server Instance
    """
    if request.method == 'POST':
        instance = models.Instance.objects.get(id = instance_id)
        instance.delete()
        return redirect('/cloud/%s' % uuid)
    
    return direct_to_template(  request,
                                'cloud/instance_delete.html',
                                {'request': request,
                                'cloud': models.Cloud.objects.get(uuid = uuid),
                                'all_roles': models.RoleRelation.objects.filter(cloud__uuid = uuid),
                                'instance': models.Instance.objects.get(id = instance_id)
                                })

@login_required
def instance_delete_ebs(request, uuid, role_id, instance_id, ebs_id):
    """
    Delete an EBSVolume
    """
    if request.method == 'POST':
        ebs = models.EBSVolume.objects.get(id = ebs_id)
        ebs.delete()
        return redirect('/cloud/%s/role/%s/instance/%s/ebs' % (  uuid, role_id, instance_id))

    return direct_to_template(  request,
                                'cloud/instance_delete_ebs.html',
                                {'request': request,
                                'cloud': models.Cloud.objects.get(uuid = uuid),
                                'role_id': role_id,
                                'instance': models.Instance.objects.get(id = instance_id),
                                'ebs': models.EBSVolume.objects.get(id = ebs_id),
                                })

@login_required
def instance_delete_elastic_ip(request, uuid, role_id, instance_id, elastic_ip_id):
    """
    Delete an ElasticIP
    """
    if request.method == 'POST':
        elastic_ip = models.ElasticIP.objects.get(id = elastic_ip_id)
        elastic_ip.delete()
        return redirect('/cloud/%s/role/%s/instance/%s/elastic_ip' % (  uuid, role_id, instance_id))

    return direct_to_template(  request,
                                'cloud/instance_delete_elastic_ip.html',
                                {'request': request,
                                'cloud': models.Cloud.objects.get(uuid = uuid),
                                'role_id': role_id,
                                'instance': models.Instance.objects.get(id = instance_id),
                                'elastic_ip': models.ElasticIP.objects.get(id = elastic_ip_id),
                                })

@login_required
def list(request):
    """
    Show the clouds registered for the authenticated user
    """
    return direct_to_template(  request,
                                'cloud/list.html',
                                {'request': request,
                                'clouds': core.models.Account.clouds(request.user),})

@login_required
def role_assign(request, uuid):
    """
    Assign roles to a cloud
    """
    message = ''
    if request.method == 'POST':
        form = forms.RoleRelationForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit = False)
            form_instance.cloud = models.Cloud.objects.get(uuid = uuid)
            print len(models.RoleRelation.objects.filter(cloud = form_instance.cloud, role = form_instance.role))
            
            if len(models.RoleRelation.objects.filter(cloud = form_instance.cloud, role = form_instance.role)) > 0:
                message = 'Role already assigned'
            else: 
                form_instance.save()
                message = 'Role added'

            return redirect('/cloud/%s' % uuid)
    else:
        form = forms.RoleRelationForm()
        form.fields['role'].queryset = models.Role.objects.filter(is_global = True)

    return direct_to_template(  request,
                                'cloud/role_assign.html',
                                {   'request': request,
                                    'form': form,
                                    'message': message,
                                    'cloud': models.Cloud.objects.get(uuid = uuid), })
