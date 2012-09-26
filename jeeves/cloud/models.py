from django.db import models
from core.models import Account
import definitions


class Cloud(models.Model):
    """
    Definition of a Cloud
    """
    def __unicode__(self):
        return self.uuid

    uuid = models.CharField(blank=False, unique=True, max_length=36)
    name = models.CharField(blank=False, max_length=30)
    aws_access_key = models.CharField(blank=False,
        max_length=30,
        verbose_name='AWS ID number')
    aws_secret_key = models.CharField(blank=False, max_length=60,
        verbose_name='AWS secret key')
    region = models.CharField(blank=False, max_length=20,
        choices=definitions.REGIONS)
    owner = models.ForeignKey(Account)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class Cluster(models.Model):
    """
    Definition of a cluster
    """
    def __unicode__(self):
        return self.name

    cloud = models.ForeignKey(Cloud)
    name = models.CharField(blank=False, max_length=30)
    description = models.TextField(blank=False)

class AutoScalingGroupDefinition(models.Model):
    """
    Definition of an auto scaling group
    """
    def __unicode__(self):
        return '%s-v%i' % (self.name, self.version)
    cluster = models.ForeignKey(Cluster)
    version = models.IntegerField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(blank=False, max_length=30)
    availability_zones = models.CharField(blank=False,
        max_length=20,
        choices=definitions.AVAILABILITY_ZONES)
    launch_config_name = models.CharField(blank=False, max_length=40)
    min_size = models.IntegerField(blank=False, default=1)
    max_size = models.IntegerField(blank=False, default=1)
