from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from account.models import AccountOwenrModel

class UserCreateSerializer(BaseUserCreateSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        AccountOwenrModel.objects.create(user=user)
        return user

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username']
