from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import TransactionModel
from account.models import AccountOwenrModel, AccountModel

# Create your views here.

class TransactionApiView(APIView):
    def get(self,request):
        user_accounts = AccountOwenrModel.objects.get(id=self.request.user.id)