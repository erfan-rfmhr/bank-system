from django.db import models
from django.conf import settings

# Create your models here.

class AccountOwenr(models.Model):
    User = models.OneToOneField(settings.USER_AUTH_MODEL , on_delete = models.CASCADE)
    phone = models.CharField(max_length = 11)

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('seporde' , 'seporde'),
        ('jari' , 'jari'),
    ]
    user = models.ForeignKey(AccountOwenr , on_delete = models.CASCADE)
    balance = models.CharField(max_length =255)
    type = models.CharField(max_length =255 , choices = ACCOUNT_TYPE_CHOICES)
    