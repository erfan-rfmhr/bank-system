from django.db import models
from django.conf import settings

# Create your models here.

class AccountOwenr(models.Model):
    User = models.OneToOneField(settings.USER_AUTH_MODEL , on_delete = models.CASCADE)
    phone = models.CharField(max_length = 11)

