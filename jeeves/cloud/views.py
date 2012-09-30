import uuid
import core
from cloud import aws
from cloud import forms
from cloud import models
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale.group import AutoScalingGroup


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
def auto_scaling_group(request, uuid):
    """
    List all auto scaling groups
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)
    conn = aws.HANDLER.get_as_connection(uuid)
    auto_scaling_groups = conn.get_all_groups()

    return direct_to_template(request,
        'cloud/auto_scaling_group.html',
        {
            'request': request,
            'cloud': cloud,
            'auto_scaling_groups': auto_scaling_groups
        })


@login_required
def auto_scaling_group_add(request, uuid):
    """
    Create a new auto scaling group
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)

    message = ''

    conn = aws.HANDLER.get_as_connection(uuid)
    lcs = conn.get_all_launch_configurations()
    launch_configurations = [('', 'None')]
    for lc in lcs:
        launch_configurations.append((lc.name, lc.name))

    if request.method == 'POST':
        form = forms.AutoScalingGroupForm(launch_configurations, request.POST)
        if form.is_valid():
            conn = aws.HANDLER.get_as_connection(uuid)
            conn.create_auto_scaling_group(AutoScalingGroup(
                group_name=form.cleaned_data['name'],
                availability_zones=form.cleaned_data['availability_zones'],
                launch_config=form.cleaned_data['launch_config_name'],
                min_size=form.cleaned_data['min_size'],
                max_size=form.cleaned_data['max_size'],))
            message = 'Your auto scaling group has been created'
            return redirect('/cloud/%s/auto_scaling_group' % cloud.uuid)
    else:
        form = forms.AutoScalingGroupForm(launch_configurations)

    return direct_to_template(request,
        'cloud/auto_scaling_group_add.html',
        {
            'request': request,
            'form': form,
            'message': message,
            'cloud': cloud
        })


@login_required
def auto_scaling_group_def_handle(request, uuid, cluster_id, asg_def_id, action):
    """
    Handle commands to an auto scaling group def
    """
    get_object_or_404(models.Cloud, uuid=uuid)
    cluster = get_object_or_404(models.Cluster, pk=cluster_id)
    asg_def = get_object_or_404(models.AutoScalingGroupDefinition,
        pk=asg_def_id)

    # Get a list of the AZs
    availability_zones = \
        [az.availability_zone for az in asg_def.availability_zones.all()]

    conn = aws.HANDLER.get_as_connection(uuid)
    if action is 'start':
        # Start the ASG
        conn.create_auto_scaling_group(AutoScalingGroup(
                    group_name='%s-%s' % (cluster.name, asg_def.version),
                    availability_zones=availability_zones,
                    launch_config=asg_def.launch_config_name,
                    min_size=asg_def.min_size,
                    max_size=asg_def.max_size,))

        # Set the ASGDef is_registered & has_instance flags to True
        asg_def.set_is_registered(True)
        asg_def.set_has_instances(True)
    elif action is 'stop_instances':
        # Stop instances
        asg = conn.get_all_groups(
            names=['%s-%s' % (cluster.name, asg_def.version)])[0]
        asg.shutdown_instances()

        # Set the ASGDef is_registered & has_instance flags to True
        asg_def.set_has_instances(False)
    elif action is 'deregister_asg':
        # Stop instances
        asg = conn.get_all_groups(
            names=['%s-%s' % (cluster.name, asg_def.version)])[0]
        asg.delete()

        # Set the ASGDef is_registered & has_instance flags to True
        asg_def.set_is_registered(False)

    return redirect('/cloud/%s/cluster/%s' % (uuid, cluster_id))


@login_required
def cluster(request, uuid):
    """
    List all clusters
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)
    return direct_to_template(request,
        'cloud/cluster.html',
        {
            'request': request,
            'cloud': cloud,
            'clusters': models.Cluster.objects.filter(cloud__uuid=uuid)
        })


@login_required
def cluster_add(request, uuid):
    """
    Create a new cluster
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)

    message = ''

    if request.method == 'POST':
        form = forms.ClusterForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.cloud = models.Cloud.objects.get(uuid=uuid)
            form_instance.save()
            message = 'Your cloud has been created'
            form = forms.CloudForm()
            return redirect('/cloud/%s/cluster' % cloud.uuid)
    else:
        form = forms.ClusterForm()

    return direct_to_template(request,
        'cloud/cluster_add.html',
        {
            'request': request,
            'form': form,
            'message': message,
            'cloud': cloud
        })


@login_required
def cluster_details(request, uuid, cluster_id):
    """
    Overview of a given cluster
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)
    cluster = get_object_or_404(models.Cluster, pk=cluster_id)
    asg_defs = models.AutoScalingGroupDefinition.objects.filter(
        cluster=cluster_id)

    return direct_to_template(request,
        'cloud/cluster_details.html',
        {
            'request': request,
            'cloud': cloud,
            'cluster': cluster,
            'asg_defs': asg_defs
        })


@login_required
def cluster_asg_def_add(request, uuid, cluster_id):
    """
    Add new auto scaling group definition
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)
    cluster = get_object_or_404(models.Cluster, pk=cluster_id)

    message = ''

    # Get the possible choices
    as_con = aws.HANDLER.get_as_connection(uuid)
    lc_choices = []
    for launch_config in as_con.get_all_launch_configurations():
        lc_choices.append((launch_config.name, launch_config.name))
    lb_choices = []
    ec2 = aws.HANDLER.get_ec2_connection(uuid)
    for address in ec2.get_all_addresses():
        lb_choices.append((
            address.public_ip,
            'Elastic IP - %s' % address.public_ip))
    elb = aws.HANDLER.get_elb_connection(uuid)
    for load_balancer in elb.get_all_load_balancers():
        lb_choices.append((
            u'%s' % load_balancer.name,
            'ELB - %s' % load_balancer.name))

    if request.method == 'POST':
        form = forms.AutoScalingGroupDefinitionForm(lc_choices,
            lb_choices, request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.cluster = models.Cluster.objects.get(pk=cluster_id)
            form_instance.save()
            message = 'New ASG definition created'

            # Now add the availability zones
            # in the many-to-amany field
            asg_def = models.AutoScalingGroupDefinition.objects.get(
                pk=form_instance.id)
            for availability_zone in form.cleaned_data['availability_zones']:
                asg_def.availability_zones.add(availability_zone)

            form = forms.CloudForm()
            return redirect('/cloud/%s/cluster/%s' % (
                cloud.uuid, cluster_id))
    else:
        form = forms.AutoScalingGroupDefinitionForm(lc_choices, lb_choices)

    return direct_to_template(request,
        'cloud/cluster_asg_def_add.html',
        {
            'request': request,
            'form': form,
            'message': message,
            'cloud': cloud,
            'cluster': cluster
        })


@login_required
def edit(request, uuid):
    """
    Edit preferences in a Cloud
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)

    if request.method == 'POST':
        form = forms.CloudForm(request.POST, instance=cloud)
        if form.is_valid():
            form.save()

            # Terminate all AWS connections for this cloud
            aws.HANDLER.terminate(uuid)

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
    cloud = get_object_or_404(models.Cloud, uuid=uuid)

    return direct_to_template(request,
        'cloud/cloud_index.html',
        {
            'request': request,
            'cloud': cloud
        })


@login_required
def launch_config(request, uuid):
    """
    List all launch configurations
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)

    conn = aws.HANDLER.get_as_connection(uuid)
    launch_configs = conn.get_all_launch_configurations()

    return direct_to_template(request,
        'cloud/launch_config.html',
        {
            'request': request,
            'cloud': cloud,
            'launch_configs': launch_configs
        })


@login_required
def launch_config_add(request, uuid):
    """
    Create a new launch configuration
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)

    message = ''

    conn = aws.HANDLER.get_ec2_connection(uuid)
    sgs = conn.get_all_security_groups()
    security_groups = []
    for sg in sgs:
        security_groups.append((sg.name, sg.name))
    keys = conn.get_all_key_pairs()
    key_pairs = []
    for key in keys:
        key_pairs.append((key.name, key.name))

    if request.method == 'POST':
        form = forms.LaunchConfigForm(security_groups, key_pairs, request.POST)
        if form.is_valid():
            conn = aws.HANDLER.get_as_connection(uuid)
            conn.create_launch_configuration(LaunchConfiguration(
                name=form.cleaned_data['name'],
                image_id=form.cleaned_data['image_id'],
                key_name=form.cleaned_data['key_name'],
                security_groups=form.cleaned_data['security_groups'],
                user_data=form.cleaned_data['user_data'],))
            message = 'Your launch config has been created'
            return redirect('/cloud/%s/launch_config' % cloud.uuid)
    else:
        form = forms.LaunchConfigForm(security_groups, key_pairs)

    return direct_to_template(request,
        'cloud/launch_config_add.html',
        {
            'request': request,
            'form': form,
            'message': message,
            'cloud': cloud
        })


@login_required
def launch_config_delete(request, uuid, launch_config_name):
    """
    Delete launch configuration
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)

    conn = aws.HANDLER.get_as_connection(uuid)
    launch_configs = conn.get_all_launch_configurations(
        names=[launch_config_name])
    if len(launch_configs) == 1:
        for launch_config in launch_configs:
            launch_config.delete()
    else:
        print "ERROR - Too many launch configs found"

    return redirect('/cloud/%s/launch_config' % cloud.uuid)


@login_required
def load_balancer(request, uuid):
    """
    List all load balancers
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)

    conn = aws.HANDLER.get_elb_connection(uuid)
    load_balancers = conn.get_all_load_balancers()

    return direct_to_template(request,
        'cloud/load_balancer.html',
        {
            'request': request,
            'cloud': cloud,
            'load_balancers': load_balancers
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
def security_group(request, uuid):
    """
    List all security groups
    """
    cloud = get_object_or_404(models.Cloud, uuid=uuid)

    conn = aws.HANDLER.get_ec2_connection(uuid)
    security_groups = conn.get_all_security_groups()
    return direct_to_template(request,
        'cloud/security_group.html',
        {
            'request': request,
            'cloud': cloud,
            'security_groups': security_groups
        })
