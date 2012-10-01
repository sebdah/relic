from django.db import models
from core.models import Account
import definitions


class Cloud(models.Model):
    """
    Definition of a Cloud
    """
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

    def __unicode__(self):
        return self.uuid


class Cluster(models.Model):
    """
    Definition of a cluster
    """
    cloud = models.ForeignKey(Cloud)
    name = models.CharField(blank=False, max_length=30)
    description = models.TextField(blank=False)

    def __unicode__(self):
        return self.name


class AvailabilityZone(models.Model):
    """
    Definition of a Availability Zone
    """
    availability_zone = models.CharField(blank=False, max_length=20)

    def __unicode__(self):
        return self.availability_zone


class AutoScalingGroupDefinition(models.Model):
    """
    Definition of an auto scaling group
    """
    class Meta:
        unique_together = ('cluster', 'version')

    cluster = models.ForeignKey(Cluster)
    created = models.DateTimeField(auto_now_add=True)
    version = models.CharField(blank=False, max_length=10, unique=True)
    availability_zones = models.ManyToManyField(AvailabilityZone)
    launch_config_name = models.CharField(blank=False, max_length=40)
    min_size = models.IntegerField(blank=False, default=1)
    max_size = models.IntegerField(blank=False, default=1)
    load_balancing_type = models.CharField(blank=False, max_length=3,
        choices=[
            ('EIP', 'Elastic IP'),
            ('ELB', 'Elastic Load Balancer')
        ])
    load_balancer = models.CharField(blank=False, max_length=60)

    # Is the ASG registered (running) @ AWS
    is_registered = models.BooleanField(default=False)

    # Are there instances running in this ASG
    has_instances = models.BooleanField(default=False)

    # Is the ASG enabled for traffic via Elastic IP or ELB?
    enabled = models.BooleanField(default=False)

    def __unicode__(self):
        return self.version

    def get_asg_name(self):
        return '%s-%s' % (self.cluster.name, self.version)

    def set_is_registered(self, val):
        self.is_registered = val

    def set_has_instances(self, val):
        self.has_instances = val
