from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import AccountOwenrModel, AccountModel
from .serializers import AccountOwnerSerializer, AccountJariCreationSerializer


class AccountOwnerUpdateView(UpdateAPIView):
    serializer_class = AccountOwnerSerializer
    queryset = AccountOwenrModel.objects.all()
    permission_classes = [IsAuthenticated]
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

