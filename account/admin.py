from django.contrib import admin
from .models import AccountOwenrModel, AccountModel

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = [ 'user','balance' ,'is_blocked' ]

admin.site.register(AccountOwenrModel)
admin.site.register(AccountModel , AccountAdmin)    