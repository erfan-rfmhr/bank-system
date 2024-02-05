from django.urls import path

from . import views

urlpatterns = [
    path('profile/<str:username>/update/', views.AdminAccountOwnerUpdateView.as_view()),
    path('jari/create/', views.AccountJariCreateView.as_view()),
    path('seporde/create/', views.AccountSepordeCreateView.as_view()),
]
