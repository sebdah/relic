from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail, create_update
from django.shortcuts import redirect
from core import forms

def index(request):
	"""
	The very index
	"""
	return direct_to_template(request, 'core/index.html')

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
