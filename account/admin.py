from django.contrib import admin
from .models import AccountOwenrModel, AccountModel

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','balance' , 'type', 'is_blocked', 'is_active' ]

admin.site.register(AccountOwenrModel)
admin.site.register(AccountModel , AccountAdmin)    