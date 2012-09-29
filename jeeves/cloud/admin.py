from cloud import models
from django.contrib import admin


class CloudAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'owner')


class AvailabilityZoneAdmin(admin.ModelAdmin):
    list_display = ('availability_zone',)

admin.site.register(models.Cloud, CloudAdmin)
admin.site.register(models.AvailabilityZone, AvailabilityZoneAdmin)
