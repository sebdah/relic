import uuid
from cloud import forms
from cloud import models
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail, create_update
from django.contrib import auth

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
    else:
        form = forms.CloudForm()

    return direct_to_template(  request,
                                'cloud/add.html',
                                {'request': request,
                                'form': form,
                                'message': message, })

@login_required
def index(request, uuid):
    """
    The overview of a single cloud
    """
    roles = models.Role.objects.filter(cloud__uuid = uuid)
    return direct_to_template(  request,
                                'cloud/index.html',
                                {'request': request,
                                'roles': roles,
                                'uuid': uuid})

@login_required
def list(request):
    """
    Show the clouds registered for the authenticated user
    
    The clouds are structured in an list like this:
    
    [[cloud1, cloud2, cloud3], [cloud4, cloud5, cloud6]...]
    """
    cloud_query = models.Cloud.objects.filter(owner = request.user).order_by('name')
    clouds = [[]]
    row = 0
    i = 0
    for cloud in cloud_query:
        clouds[row].append(cloud)
        
        if i == 2:
            i = 0
            row += 1
            clouds.append([])
        else:
            i += 1
    
    print clouds
    return direct_to_template(  request,
                                'cloud/list.html',
                                {'request': request,
                                'clouds': clouds,
                                'num_clouds': len(cloud_query) })
