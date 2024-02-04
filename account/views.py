from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import AccountOwenrModel
from .serializers import AccountOwnerSerializer


class AccountOwnerUpdateView(UpdateAPIView):
    serializer_class = AccountOwnerSerializer
    queryset = AccountOwenrModel.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'
