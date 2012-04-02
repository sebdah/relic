import uuid
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
def index(request, uuid):
    """
    The overview of a single cloud
    """
    # Get the Cloud object
    try:
        cloud = models.Cloud.objects.get(uuid = uuid)
    except models.Cloud.DoesNotExist:
        raise Http404 

    # Get the role relations (cloud <-> role) for this cloud
    role_relations = models.RoleRelation.objects.filter(cloud__uuid = uuid)
    
    # Then loop over each relation to pick out the role object
    roles = []
    for role_relation in role_relations:
        roles.append(role_relation.role)
    
    # Get instances for each role [{'role.name': [instance, n..]}]
    instances = []
    for role in roles:
        role_instances = []
        for instance in models.Instance.objects.filter(role = role):
            role_instances.append(instance)
        
        if len(role_instances) > 0:
            instances.append({role: role_instances})
    
    print instances
    return direct_to_template(  request,
                                'cloud/index.html',
                                {'request': request,
                                'roles': roles,
                                'cloud': models.Cloud.objects.get(uuid = uuid)})

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
