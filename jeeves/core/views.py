from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from core import forms

def index(request):
    return direct_to_template(request, 'core/index.html')

def register(request):
	if request.method == 'POST':
		form = forms.AccountForm(request.POST)
		
		if form.is_valid():
			form.save()
			HttpResponseRedirect("http://www.google.com")
	else:
		form = forms.AccountForm()

	return direct_to_template(	request,
    							'core/register.html',
    							{'form': form})