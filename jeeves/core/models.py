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
    last_updated        = models.DateTimeField(auto_now = True)
    registered          = models.DateTimeField(auto_now_add = True)
    is_active           = models.BooleanField(default = True)
    
    # Added for the admin site to work. Should NEVER be True
    is_staff            = False
    
    # Authentication methods
    is_authenticated    = False
    def is_authenticated(self):
        return self.is_authenticated

class Cloud(models.Model):
    """
    Definition of a Cloud
    """
    def __unicode__(self):
        return self.name
    
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
