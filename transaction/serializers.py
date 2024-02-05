from rest_framework import serializers
from rest_framework.response import Response
from .models import TransactionModel
from account.models import AccountOwenrModel , AccountModel 
from core.models import User
from django.utils import timezone
from datetime import timedelta

class TransactionSerializers(serializers.ModelSerializer):
    sender = serializers.CharField(read_only = True)
    class Meta:
        model = TransactionModel
        fields = ['id' ,'sender' , 'receiver','balance']

    def create(self, validated_data):
        sender = AccountOwenrModel.objects.get(user = self.context['request'].user)

        try:

            sender_account = AccountModel.objects.select_for_update().get(user = sender , type ='jari')
            receiver_account = AccountModel.objects.get(id =validated_data['receiver'].id )

        except AccountOwenrModel.DoesNotExist:
            raise serializers.ValidationError('کابر با این مشخصات وجود ندارد')
        except AccountModel.DoesNotExist:
            raise serializers.ValidationError('حسابی با این مشخصات وجود ندارد')

        if sender_account.id == receiver_account.id or sender_account.user == receiver_account.user:
            raise serializers.ValidationError('شما نمی‌توانید به خودتان وجه ارسال کنید.')
        
        if receiver_account.type == 'seporde':
            raise serializers.ValidationError('شما نمیتوانید به حساب از نوع  سپرده پول واریز کنید')
        if not receiver_account.is_active:
            raise serializers.ValidationError('حساب مقصد غیر فعال میباشد')
        if  sender_account.balance >= validated_data['balance']:
            if validated_data['balance'] >= 10000  :
                transaction = TransactionModel.objects.create(
                    sender = sender_account,
                    balance = validated_data['balance'],
                    receiver = validated_data['receiver'] 
                )

                sender_account.balance -= validated_data['balance']
                receiver_account.balance += validated_data['balance']

                sender_account.save()
                receiver_account.save()

                return transaction
            else:
                raise serializers.ValidationError   ('حداق مقداز تراکنش 10000 تومن میباشد')
        else:
            raise serializers.ValidationError('موجودی کافی نمیباشد')
        
class TransferSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only =True)
    blocked_until = serializers.DateField(read_only =True)
    type = serializers.CharField(read_only =True)
    class Meta:
        model = AccountModel
        fields = ['user_id' , 'balance'  , 'blocked_until' , 'type'  ]

    def save(self, **kwargs):

        try:
            loged_in_user = AccountOwenrModel.objects.get(user= self.context['request'].user)
            account_jari = AccountModel.objects.get(user = loged_in_user , type ='jari' )
            account_seporde = AccountModel.objects.get(user = loged_in_user , type ='seporde' )
            amount = self.validated_data['balance']

        except AccountModel.DoesNotExist:
            raise serializers.ValidationError('حسابی یافت نشد')
        

        if account_jari.balance >= amount:

            account_jari.balance -= amount
            account_seporde.balance += amount

            account_seporde.is_blocked =True
            account_seporde.blocked_until = timezone.now() + timedelta(days=30)

            account_jari.save()
            account_seporde.save()

            self.instance = account_jari
        else:
            raise serializers.ValidationError("موجودی حساب کافی نیست")
        
        return self.instance