from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import TransactionModel
from account.models import AccountOwenrModel, AccountModel
from .serializers import TransactionSerializers , TransferSerializer
from rest_framework import serializers
# Create your views here.

# class TransactionApiView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self,request):

#         loged_in_user = AccountOwenrModel.objects.get(user =self.request.user) 
#         account = AccountModel.objects.get(user = loged_in_user , type ='jari')
#         queryset = TransactionModel.objects.filter(sender= account).order_by('-created_at')[:10]
#         serializer = TransactionSerializers(queryset , many =True)
#         return Response(serializer.data)

    
#     def post(self,request):
#         serializer = TransactionSerializers(data= request.data , context = {'request' : request})
#         serializer.is_valid(raise_exception=True)
#         transaction = serializer.save()
#         return Response(serializer.data )
    
class TransactionApiView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializers

    def get_queryset(self):
        
        loged_in_user = AccountOwenrModel.objects.get(user =self.request.user)
        try:
            account = AccountModel.objects.get(user = loged_in_user , type ='jari')
        except AccountModel.DoesNotExist:
            raise serializers.ValidationError('حسابی با این مشخصات وجود ندارد')
        queryset = TransactionModel.objects.filter(sender= account).order_by('-created_at')[:10]

        return queryset
    def get_serializer_context(self):
        return {'request' : self.request}


    def retrieve(self, request, *args, **kwargs):
        try:
            instance = TransactionModel.objects.get(id = kwargs['pk'])
        except TransactionModel.DoesNotExist:
            return Response({'detail' : 'Not found'}, status = 404)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class TransferJari2Sepordeview(ModelViewSet):
    permission_classes = [IsAuthenticated
                          ]
    serializer_class = TransferSerializer
    def get_queryset(self):

        loged_in_user = AccountOwenrModel.objects.get(user= self.request.user)
        queryset = AccountModel.objects.filter(user = loged_in_user )

        return queryset
    
    def get_serializer_context(self):

        return {'request' : self.request }
    

