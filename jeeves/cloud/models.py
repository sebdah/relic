from django.db import models
from core.models import Account
import definitions

from boto import ec2


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
    region = models.CharField(blank=False, max_length=20,
        choices=definitions.REGIONS)
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

    def add_to_aws(self):
        """
        Add this SG to AWS
        """
        conn = ec2.connect_to_region(
            self.cloud.region,
            aws_access_key_id=self.cloud.aws_id,
            aws_secret_access_key=self.cloud.aws_secret)
        conn.create_security_group(
            self.name,
            self.description)
