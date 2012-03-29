from core import models

class JeevesAuthenticationBackend(object):
    def authenticate(self, username = None, password = None):
        """
        Authenticate a user
    
        Returns a Account object if valid, None otherwise
        """
        try:
            account = models.Account.objects.get(email = username)
            if account.password == password:
                return account
            else:
                return None
        except models.Account.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        """
        Returns a user object
        """
        try:
            return models.Account.objects.get(pk = user_id)
        except models.Account.DoesNotExist:
            return None
