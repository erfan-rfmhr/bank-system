from django.contrib import admin
from .models import TransactionModel

# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['balance' ]
admin.site.register(TransactionModel , TransactionAdmin)