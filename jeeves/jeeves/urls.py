import settings
from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    # Redirect login attempts
    (r'^accounts/login', redirect_to, {'url': '/account/login'}),
    
    url(r'^$', 'core.views.index', name='root'),
    
    url(r'^account$', 'core.views.account_index', name = 'account'),
    url(r'^account/edit$', 'core.views.account_edit'),
    url(r'^account/delete/(?P<account_id>[\w-]+)$', 'core.views.account_delete'),
    url(r'^account/login$', 'core.views.account_login'),
    url(r'^account/logout$', 'core.views.account_logout'),
    url(r'^account/register$', 'core.views.account_register'),
    url(r'^account/register/complete$', 'core.views.account_register_complete'),
    
    url(r'^cloud$', 'cloud.views.list', name = 'cloud'),
    url(r'^cloud/add$', 'cloud.views.add'),
    url(r'^cloud/(?P<uuid>[\w-]+)$', 'cloud.views.index'),
    url(r'^cloud/(?P<uuid>[\w-]+)/edit$', 'cloud.views.edit'),
    url(r'^cloud/(?P<uuid>[\w-]+)/role/assign$', 'cloud.views.role_assign'),
    url(r'^cloud/(?P<uuid>[\w-]+)/role/(?P<role_id>[\w-]+)/instance/add$', 'cloud.views.instance_add'),
    url(r'^cloud/(?P<uuid>[\w-]+)/role/(?P<role_id>[\w-]+)/instance/(?P<instance_id>[\w-]+)$', 'cloud.views.instance_view'),
    url(r'^cloud/(?P<uuid>[\w-]+)/role/(?P<role_id>[\w-]+)/instance/(?P<instance_id>[\w-]+)/ebs$', 'cloud.views.instance_edit_ebs'),
    url(r'^cloud/(?P<uuid>[\w-]+)/role/(?P<role_id>[\w-]+)/instance/(?P<instance_id>[\w-]+)/ebs/(?P<ebs_id>[\w-]+)/delete$', 'cloud.views.instance_delete_ebs'),
    url(r'^cloud/(?P<uuid>[\w-]+)/role/(?P<role_id>[\w-]+)/instance/(?P<instance_id>[\w-]+)/elastic_ip$', 'cloud.views.instance_edit_elastic_ip'),
    url(r'^cloud/(?P<uuid>[\w-]+)/role/(?P<role_id>[\w-]+)/instance/(?P<instance_id>[\w-]+)/elastic_ip/(?P<elastic_ip_id>[\w-]+)/delete$', 'cloud.views.instance_delete_elastic_ip'),
    url(r'^cloud/(?P<uuid>[\w-]+)/role/(?P<role_id>[\w-]+)/instance/(?P<instance_id>[\w-]+)/delete$', 'cloud.views.instance_delete'),
    
    url(r'^admin/', include(admin.site.urls)),
)
