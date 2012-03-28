from core import forms
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail, create_update
from django.contrib.auth import authenticate, login, logout

def index(request):
	"""
	The very index
	"""
	return direct_to_template(request, 'core/index.html')

def login(request):
    """
    Method for logging in to Jeeves
    """
    error = False
    error_message = None

    if request.method == 'POST':
    	account = authenticate(	username = request.POST['email'],
        						password = request.POST['password'])
        
        if account is not None:
            if account.is_active:
                login(request)
                return redirect("/success")
            else:
                error = True
                error_message = "Your account has been disabled!"
        else:
            error = True
            error_message = "Your username and password were incorrect."
    
    return direct_to_template(	request,
    							'core/login.html',
    							{'form': forms.AuthenticationForm(),
    							'error': error,
    							'error_message': error_message})

def register(request):
	"""
	Registration form for a new Jeeves account
	"""
	return create_update.create_object(
        request,
        login_required = False,
        form_class = forms.AccountForm,
        post_save_redirect = "/register/complete",
        template_name ="core/register.html",
        extra_context = {}
        )

def register_complete(request):
	"""
	This is the page users are redirected to after
	a successful account registration
	"""
	return direct_to_template(request, 'core/register_complete.html')
