from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.utils import IntegrityError
from .models import AccountOwenrModel, AccountModel


class AdminCreateAccountOwnerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(
        source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(
        source='user.last_name', required=False, allow_blank=True)

    class Meta:
        model = AccountOwenrModel
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'username', 'email', 'password']

    def create(self, validated_data):
        user_model = get_user_model()
        user_data = validated_data.pop('user', {})
        try:
            user = user_model.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', '')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {'username': 'کاربر با این مشخصات وجود دارد.'})
        account_owner = AccountOwenrModel.objects.create(
            user=user,
            phone_number=validated_data['phone_number']
        )
        return account_owner


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

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user', {})
    #     user = AccountOwenrModel.objects.create(**validated_data)
    #     user.first_name = user_data.get('first_name', user.first_name)
    #     user.last_name = user_data.get('last_name', user.last_name)
    #     user.save()
    #     return user


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


class AccountSepordeCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = ['id', 'balance', 'type']
        read_only_fields = ['id', 'type']

    def create(self, validated_data):
        user = self.context['request'].user
        account = AccountModel.objects.create(
            user=user.account_owner,
            balance=validated_data['balance'],
            type='seporde'
        )
        return account


class AccountSerializer(serializers.ModelSerializer):
    user = AccountOwnerSerializer(read_only=True)

    class Meta:
        model = AccountModel
        fields = ['id', 'user', 'balance', 'type', 'is_blocked', 'created_at', 'is_active', 'blocked_until']
        read_only_fields = ['id', 'user', 'created_at', 'is_active', 'blocked_until']
