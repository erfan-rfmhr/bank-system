from django.db import models
from account.models import  AccountModel
# Create your models here.

class TransactionModel(models.Model):
    sender = models.ForeignKey(AccountModel , on_delete = models.CASCADE , related_name =   'sender')
    receiver = models.ForeignKey(AccountModel , on_delete = models.CASCADE , related_name = 'receiver')
    balance = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)