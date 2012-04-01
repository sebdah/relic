import uuid
from core import forms
from core import models
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
    return direct_to_template(request, 'core/account/index.html', {'request': request})

@login_required
def account_edit(request):
    """
    Edit account settings
    """
    message = ""
    account = models.Account.objects.get(id = request.user.id)
    
    if request.method == 'POST':
        form = forms.AccountForm(request.POST, instance = account)
        if form.is_valid():
            form.save()
            message = 'Your profile has been updated'
    else:
        form = forms.AccountForm(instance = account)
    
    return direct_to_template(  request,
                                'core/account/edit.html',
                                {   'request': request, 
                                    'form': form,
                                    'message': message})

@login_required
def account_delete(request, account_id):
    """
    Delete an account given the ID
    """
    account = models.Account.objects.get(id = account_id)
    account.delete()
    auth.logout(request)
    return redirect('/')

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
                                'core/account/login.html',
                                {'form': forms.AuthenticationForm(),
                                'error': error,
                                'error_message': error_message,
                                'request': request})

def account_logout(request):
    """
    Logout an Account
    """
    auth.logout(request)
    return direct_to_template(request, 'core/account/logout.html', {'request': request})

def account_register(request):
    """
    Registration form for a new Jeeves account
    """
    return create_update.create_object(
        request,
        login_required = False,
        form_class = forms.AccountForm,
        post_save_redirect = "/account/register/complete",
        template_name ="core/account/register.html",
        extra_context = {'request': request}
        )

def account_register_complete(request):
    """
    This is the page users are redirected to after
    a successful account registration
    """
    return direct_to_template(request, 'core/account/register_complete.html', {'request': request})

@login_required
def cloud_add(request):
    """
    Create a new cloud
    """
    message = ''
    if request.method == 'POST':
        form = forms.CloudForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit = False)
            form_instance.owner = request.user
            form_instance.uuid = uuid.uuid4()
            form_instance.save()
            message = 'Your cloud has been created'
            form = forms.CloudForm()
    else:
        form = forms.CloudForm()

    return direct_to_template(  request,
                                'core/cloud/add.html',
                                {'request': request,
                                'form': form,
                                'message': message, })

@login_required
def cloud_index(request):
    """
    Show the clouds registered for the authenticated user
    """
    clouds = models.Cloud.objects.filter(owner = request.user).order_by('name')
    return direct_to_template(  request,
                                'core/cloud/index.html',
                                {'request': request,
                                'clouds': clouds })

def index(request):
    """
    The very index
    """
    return direct_to_template(request, 'core/index.html', {'request': request})
