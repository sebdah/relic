from core import forms
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail, create_update
from django.contrib import auth

@login_required
def account_index(request):
    """
    The 'startpage' for logged in users
    """
    return direct_to_template(request, 'core/account_index.html', {'request': request})

def account_login(request):
    """
    Method for logging in to Jeeves
    """
    error = False
    error_message = None

    if request.method == 'POST':
        account = auth.authenticate(username = request.POST['email'],
                                    password = request.POST['password'])
        
        if account:
            if account.is_active:
                auth.login(request, account)
                return redirect("/account")
            else:
                error = True
                error_message = "Your account has been disabled!"
        else:
            error = True
            error_message = "Your username and password were incorrect."
    
    return direct_to_template(  request,
                                'core/account_login.html',
                                {'form': forms.AuthenticationForm(),
                                'error': error,
                                'error_message': error_message,
                                'request': request})

def account_logout(request):
    """
    Logout an Account
    """
    auth.logout(request)
    return direct_to_template(request, 'core/account_logout.html', {'request': request})

def account_register(request):
    """
    Registration form for a new Jeeves account
    """
    return create_update.create_object(
        request,
        login_required = False,
        form_class = forms.AccountForm,
        post_save_redirect = "/account/register/complete",
        template_name ="core/account_register.html",
        extra_context = {'request': request}
        )

def account_register_complete(request):
    """
    This is the page users are redirected to after
    a successful account registration
    """
    return direct_to_template(request, 'core/account_register_complete.html', {'request': request})

def index(request):
    """
    The very index
    """
    return direct_to_template(request, 'core/index.html', {'request': request})