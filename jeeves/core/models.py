from django.db import models
import cloud

class Account(models.Model):
    """
    Definition of an Account
    """
    def __unicode__(self):
        return self.email
    
    email               = models.EmailField(blank = False, unique = True)
    password            = models.CharField(blank = False, max_length = 50)
    first_name          = models.CharField(blank = False, max_length = 50)
    last_name           = models.CharField(blank = False, max_length = 50)
    last_updated        = models.DateTimeField(auto_now = True)
    registered          = models.DateTimeField(auto_now_add = True)
    is_active           = models.BooleanField(default = True)
    
    # Added for the admin site to work. Should NEVER be True
    is_staff            = False
    
    # Authentication methods
    is_authenticated    = False
    def is_authenticated(self):
        return self.is_authenticated
    
    def clouds(self):
        """
        Return all Cloud objects related to this Account
        """
        return cloud.models.Cloud.objects.filter(owner = self.id).order_by('name')

