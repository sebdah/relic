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

class Role(models.Model):
    """
    Defines a Role
    """
    def __unicode__(self):
        return self.name

    name                = models.CharField(blank = False, max_length = 30)
    cloud               = models.ForeignKey(Cloud)

class Instance(models.Model):
    """
    Definition of an instance
    """
    def __unicode__(self):
        return self.hostname
    
    role                = models.ForeignKey(Role)
    hostname            = models.CharField( blank = False,
                                            max_length = 30)
    instance_id         = models.CharField(max_length = 10)
    instance_type       = models.CharField( blank = False,
                                            max_length = 10,
                                            choices = definitions.INSTANCE_TYPES)
    availability_zone   = models.CharField( blank = False,
                                            max_length = 10,
                                            choices = definitions.AVAILABILITY_ZONES)

class Package(models.Model):
    """
    Defines a OS package
    """
    def __unicode__(self):
        return self.name
    
    name                = models.CharField(blank = False, max_length = 60)
    role                = models.ForeignKey(Role)

class EBSVolume(models.Model):
    """
    Define an EBS volume
    """
    def __unicode__(self):
        return "%s (%i GB)" % (self.mountpoint, self.size)
    
    mountpoint          = models.CharField(blank = False, max_length = 250)
    size                = models.IntegerField(blank = False, default = 10)
    role                = models.ForeignKey(Role)

class ElasticIP(models.Model):
    """
    Definition of an Elastic IP
    """
    def __unicode__(self):
        return self.dns_name
    
    dns_name            = models.CharField(blank = False, max_length = 250)
    role                = models.ForeignKey(Role)
