from rest_framework import serializers
from rest_framework.response import Response
from .models import TransactionModel
from account.models import AccountOwenrModel , AccountModel 
from core.models import User
class TransactionSerializers(serializers.ModelSerializer):
    sender = serializers.CharField(read_only = True)
    class Meta:
        model = TransactionModel
        fields = ['id' ,'sender' , 'receiver','balance']

    def create(self, validated_data):
        sender = AccountOwenrModel.objects.get(user = self.context['request'].user)
        # receiver = 
        # receiver = AccountModel.objects.get(user =User.objects.get(id= validated_data['receiver'].id))
        # receiver = AccountModel.objects.filter(user_id = "2")
        # print(receiver)
        # print(validated_data['receiver'].id)
        try:

            sender_account = AccountModel.objects.select_for_update().get(user = sender , type ='jari')
            receiver_account = AccountModel.objects.get(id =validated_data['receiver'].id )
            # receiver_account = AccountModel.objects.select_for_update().get(user = receiver , type ='jari')
            print("------------")
            print(sender_account.id , validated_data['receiver'].id)


        except AccountOwenrModel.DoesNotExist:

            raise serializers.ValidationError('کابر با این مشخصات وجود ندارد')
        
        if sender_account.id == receiver_account.id:
            raise serializers.ValidationError('شما نمی‌توانید به خودتان وجه ارسال کنید.')
        
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