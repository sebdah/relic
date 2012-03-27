from django.views.generic.simple import direct_to_template

def index(request):
    return direct_to_template(request, 'core/index.html')

def register(request):
    return direct_to_template(request, 'core/register.html')