from django.db import models
from django.conf import settings
from django.contrib import admin
# Create your models here.
class AccountOwenrModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete = models.CASCADE)
    phone_number = models.CharField(max_length = 11 )

    # @admin.display("user__username")
    def __str__(self) :
        return self.user.username

class AccountModel(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('seporde' , 'seporde'),
        ('jari' , 'jari'),
    ]
    user = models.ForeignKey(AccountOwenrModel , on_delete = models.CASCADE)
    balance = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length =255 , choices = ACCOUNT_TYPE_CHOICES)
    is_blocked = models.BooleanField(default =False)
    created_at = models.DateTimeField(auto_now_add=True)

    blocked_until = models.DateField(null =True , blank = True)

    def __str__(self) -> str:
        return f"{self.user}"