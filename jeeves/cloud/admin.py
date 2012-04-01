from cloud import models
from django.contrib import admin

class CloudAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'owner')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('cloud', 'name', 'is_global')
    list_filter = ('is_global',)

class InstanceAdmin(admin.ModelAdmin):
    list_display = ('role', 'hostname', 'instance_id', 'availability_zone')
    list_filter = ('availability_zone',)
    
class PackageAdmin(admin.ModelAdmin):
    list_display = ('role', 'name')
    
class EBSVolumeAdmin(admin.ModelAdmin):
    list_display = ('role', 'mountpoint', 'size')
    
class ElasticIPAdmin(admin.ModelAdmin):
    list_display = ('role', 'dns_name')

admin.site.register(models.Cloud, CloudAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Instance, InstanceAdmin)
admin.site.register(models.Package, PackageAdmin)
admin.site.register(models.EBSVolume, EBSVolumeAdmin)
admin.site.register(models.ElasticIP, ElasticIPAdmin)
