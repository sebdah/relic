from django.db import models
from core.models import Account
from boto import ec2
from cloud import definitions

class Cloud(models.Model):
    """
    Definition of a Cloud
    """
    def __unicode__(self):
        return self.uuid
    
    uuid                = models.CharField(blank = False, unique = True, max_length = 36)
    name                = models.CharField(blank = False, max_length = 30)
    aws_id              = models.CharField( blank = False,
                                            max_length = 30,
                                            verbose_name = 'AWS ID number')
    aws_secret          = models.CharField( blank = False,
                                            max_length = 60,
                                            verbose_name = 'AWS secret key')
    owner               = models.ForeignKey(Account)
    created             = models.DateTimeField(auto_now_add = True)
    last_updated        = models.DateTimeField(auto_now = True)
    is_active           = models.BooleanField(default = True)
    
    def instances(self):
        """
        Return all Instances linked to this cloud
        """
        return Instance.objects.filter(cloud__uuid = self.uuid).order_by('hostname')
    
    def roles(self):
        """
        Return all Role objects matching this cloud
        """
        roles = []
        for role_relation in RoleRelation.objects.filter(cloud__uuid = self.uuid).order_by('role__name'):
            roles.append(Role.objects.get(id = role_relation.role.id))
        return roles
    
    def role_instances(self):
        """
        Return a dict with [{'role': [instance, instance..]}]
        """
        instances = []

        for role in self.roles():
            role_instances = []
            for instance in Instance.objects.filter(role = role).order_by('hostname'):
                role_instances.append(instance)

            if len(role_instances) > 0:
                instances.append({role: role_instances})
        
        return instances

class Role(models.Model):
    """
    Defines a Role
    """
    def __unicode__(self):
        return self.name

    name                = models.CharField(blank = False, max_length = 30)
    is_global           = models.BooleanField(default = False)

class RoleRelation(models.Model):
    """
    Defines which cloud has which role
    """
    cloud               = models.ForeignKey(Cloud)
    role                = models.ForeignKey(Role)

class Instance(models.Model):
    """
    Definition of an instance
    """
    def __unicode__(self):
        return self.hostname
    
    role                = models.ForeignKey(Role)
    cloud               = models.ForeignKey(Cloud)
    hostname            = models.CharField( blank = False,
                                            max_length = 30)
    instance_id         = models.CharField( max_length = 10,
                                            verbose_name = 'Instance ID')
    instance_type       = models.CharField( blank = False,
                                            max_length = 10,
                                            choices = definitions.INSTANCE_TYPES)
    availability_zone   = models.CharField( blank = False,
                                            max_length = 20,
                                            choices = definitions.AVAILABILITY_ZONES)
    
    def ebs_volumes(self):
        """
        Return all EBS volumes related to this Instance
        """
        return EBSVolume.objects.filter(instance = self.id)
    
    def elastic_ips(self):
        """
        Return all Elastic IP's related to this Instance
        """
        return ElasticIP.objects.filter(instance = self.id)

class Package(models.Model):
    """
    Defines a OS package
    """
    def __unicode__(self):
        return self.name
    
    name                = models.CharField(blank = False, max_length = 60)
    role                = models.ForeignKey(Role)
    cloud               = models.ForeignKey(Cloud)

class EBSVolume(models.Model):
    """
    Define an EBS volume
    """
    def __unicode__(self):
        return "%s (%i GB)" % (self.mountpoint, self.size)
    
    mountpoint          = models.CharField(blank = False, max_length = 250)
    size                = models.IntegerField(  blank = False, default = 10,
                                                verbose_name = 'Size (GB)')
    instance            = models.ForeignKey(Instance)
    cloud               = models.ForeignKey(Cloud)

class ElasticIP(models.Model):
    """
    Definition of an Elastic IP
    """
    def __unicode__(self):
        return self.dns_name
    
    dns_name            = models.CharField( blank = False, max_length = 250,
                                            verbose_name = 'DNS name')
    instance            = models.ForeignKey(Instance)
    cloud               = models.ForeignKey(Cloud)
