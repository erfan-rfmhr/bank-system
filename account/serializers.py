from rest_framework import serializers
from core.models import User
from .models import AccountOwenrModel


class AccountOwnerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.first_name', required=False)
    last_name = serializers.CharField(
        source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = AccountOwenrModel
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        user_data = validated_data.pop('user', {})
        print(user_data)
        instance.user.first_name = user_data.get(
            'first_name', instance.user.first_name)
        instance.user.last_name = user_data.get(
            'last_name', instance.user.last_name)

        instance.save()
        instance.user.save()
        return instance

    def create(self, validated_data):
        user_id = self.context['user_id']
        user = User.objects.get(id=user_id)
        if not AccountOwenrModel.objects.filter(user_id=user_id).exists():
            return AccountOwenrModel.objects.create(id=user_id, user=user, ** validated_data)
        else:
            raise serializers.ValidationError(
                "such a profile already exist")
