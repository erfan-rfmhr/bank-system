# urls.py

from django.urls import path
from . import views
urlpatterns = [
    path('profile/<str:username>/update/', views.AccountOwnerUpdateView.as_view()),
]
