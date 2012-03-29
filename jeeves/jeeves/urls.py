import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^$', 'core.views.index'),
    
    url(r'^account$', 'core.views.account_index'),
    url(r'^account/login$', 'core.views.account_login'),
    url(r'^account/logout$', 'core.views.account_logout'),
    url(r'^account/register$', 'core.views.account_register'),
    url(r'^account/register/complete$', 'core.views.account_register_complete'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
