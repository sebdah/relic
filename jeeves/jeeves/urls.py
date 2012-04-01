import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^$', 'core.views.index'),
    
    url(r'^account$', 'core.views.account_index'),
    url(r'^account/edit$', 'core.views.account_edit'),
    url(r'^account/delete/(?P<account_id>[\w-]+)$', 'core.views.account_delete'),
    url(r'^account/login$', 'core.views.account_login'),
    url(r'^account/logout$', 'core.views.account_logout'),
    url(r'^account/register$', 'core.views.account_register'),
    url(r'^account/register/complete$', 'core.views.account_register_complete'),
    
    url(r'^cloud$', 'cloud.views.list'),
    url(r'^cloud/add$', 'cloud.views.add'),
    url(r'^cloud/(?P<uuid>[\w-]+)$', 'cloud.views.index'),
    
    url(r'^admin/', include(admin.site.urls)),
)
