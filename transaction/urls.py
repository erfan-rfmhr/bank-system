from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register("transaction" , views.TransactionApiView , basename = 'transaction')
router.register('Jari_to_seporde' , views.TransferJari2Sepordeview , basename="transfer_jari2seporde")


urlpatterns = [
    # path('transaction' , views.TransactionApiView.as_view() , name ='transaction'),
]

urlpatterns+= router.urls 