from cloud import models
from django.contrib import admin

class CloudAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'owner')

admin.site.register(models.Cloud, CloudAdmin)
