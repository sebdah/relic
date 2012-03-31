from core import models
from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    #fields = ['email', 'first_name', 'last_name']

class CloudAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'owner')

admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Cloud, CloudAdmin)
