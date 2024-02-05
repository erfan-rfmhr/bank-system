from rest_framework import serializers

from .models import AccountOwenrModel, AccountModel


class AccountOwnerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(
        source='user.last_name', required=False, allow_blank=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = AccountOwenrModel
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.save()
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        user = AccountOwenrModel.objects.create(**validated_data)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()
        return user


class AccountJariCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = ['id', 'balance', 'type']
        read_only_fields = ['id', 'type']

    def create(self, validated_data):
        user = self.context['request'].user
        account = AccountModel.objects.create(
            user=user.account_owner,
            balance=validated_data['balance'],
            type='jari'
        )
        return account
