from django.db import models
from core.models import AccountModel

# Create your models here.

class TransactionModel(models.Model):
    sender = models.ForeignKey(AccountModel , on_delete = models.CASCADE)
    receiver = models.ForeignKey(AccountModel , on_delete = models.CASCADE)
    balance = models.CharField(max_length = 255)