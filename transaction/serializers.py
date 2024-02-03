from rest_framework import serializers
from .models import TransactionModel


class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = ['id' ,'sender' , 'receiver','balance']