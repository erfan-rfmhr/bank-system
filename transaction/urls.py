from . import views
from django.urls import path

urlpatterns = [
    path('transaction' , views.TransactionApiView.as_view() , name ='transaction')
]