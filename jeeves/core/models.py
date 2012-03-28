from django.db import models

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
    last_updated        = models.DateTimeField(blank = True, auto_now = True)
    registered          = models.DateTimeField(blank = True, auto_now_add = True)
    is_active           = models.BooleanField(default = True)
