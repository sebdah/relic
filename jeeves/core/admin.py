from core.models import Account
from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    #fields = ['email', 'first_name', 'last_name']

admin.site.register(Account, AccountAdmin)
