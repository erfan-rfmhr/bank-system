from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import TransactionModel
from account.models import AccountOwenrModel, AccountModel
from .serializers import TransactionSerializers
# Create your views here.

class TransactionApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):

        loged_in_user = AccountOwenrModel.objects.get(user =self.request.user) 
        account = AccountModel.objects.get(user = loged_in_user , type ='jari')
        queryset = TransactionModel.objects.filter(sender= account).order_by('-created_at')[:10]
        serializer = TransactionSerializers(queryset , many =True)
        return Response(serializer.data)

    
    def post(self,request):
        serializer = TransactionSerializers(data= request.data , context = {'request' : request})
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        return Response(serializer.data )
