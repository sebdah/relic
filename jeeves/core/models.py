import uuid
import cloud
from jeeves import settings
from django.db import models
from django.core.mail import send_mail

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
    is_active           = models.BooleanField(default = False)
    activation_key      = models.CharField(blank = True, null = True, max_length = 50)
    
    # Added for the admin site to work. Should NEVER be True
    is_staff            = False
    
    is_authenticated    = False
    def is_authenticated(self):
        return self.is_authenticated
    
    def activate(self):
        """
        Activate account
        """
        self.is_active = True
        
        return self.save()
    
    def clouds(self):
        """
        Return all Cloud objects related to this Account
        """
        return cloud.models.Cloud.objects.filter(owner = self.id).order_by('name')
    
    def save(self, *args, **kwargs):
         """
         Save a new account
         """
         # Generate activation key
         self.activation_key = uuid.uuid4()
         
         # Send activation e-mail
         message = """\
Welcome to Jeeves, %s\n\n
You (or somebody else) has registrered an account for %s at Jeeves cloud management. Please follow
the below link in order to activate your account.\n\n

%s/account/confirm/%s\n\n

Best regards\n
Jeeves Team
""" % (self.first_name, self.email, settings.JEEVES_EXTERNAL_URL, self.activation_key)
         send_mail( 'Activate your Jeeves account',
                    message, settings.JEEVES_NO_REPLY_ADDRESS,
                    [self.email], fail_silently = False)
         
         # Save the object
         super(Account, self).save(*args,**kwargs)

