from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AccountOwenrModel, AccountModel
from .serializers import AccountOwnerSerializer, AccountJariCreationSerializer, AccountSepordeCreationSerializer


class AdminAccountOwnerUpdateView(UpdateAPIView):
    serializer_class = AccountOwnerSerializer
    queryset = AccountOwenrModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'


class AccountJariCreateView(CreateAPIView):
    serializer_class = AccountJariCreationSerializer
    queryset = AccountModel.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        account = AccountModel.objects.filter(user=user.account_owner, type='jari')
        if not account.exists():
            return super().create(request, *args, **kwargs)
        return Response({'detail': 'شما در حال حاضر یک حساب جاری دارید.'}, status=400)


class AccountSepordeCreateView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        account = AccountModel.objects.filter(user=user.account_owner, type='seporde')
        if account.exists():
            return Response({'detail': 'شما در حال حاضر یک حساب سپرده دارید.'}, status=400)

        account = AccountModel.objects.create(user=user.account_owner, type='seporde')
        serializer = AccountSepordeCreationSerializer(account)
        return Response(serializer.data, status=201)
