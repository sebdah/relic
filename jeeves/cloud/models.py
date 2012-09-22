from django.db import models
from core.models import Account


class Cloud(models.Model):
    """
    Definition of a Cloud
    """
    def __unicode__(self):
        return self.uuid

    uuid = models.CharField(blank=False, unique=True, max_length=36)
    name = models.CharField(blank=False, max_length=30)
    aws_id = models.CharField(blank=False,
        max_length=30,
        verbose_name='AWS ID number')
    aws_secret = models.CharField(blank=False, max_length=60,
        verbose_name='AWS secret key')
    owner = models.ForeignKey(Account)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class SecurityGroup(models.Model):
    """
    Definition of a security group
    """
    def __unicode__(self):
        return self.name

    cloud = models.ForeignKey(Cloud)
    name = models.CharField(blank=False, max_length=30)
    description = models.CharField(blank=False, max_length=60)
