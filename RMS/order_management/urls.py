from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test

urlpatterns = [
    path('order-management/', views.order_management, name='order_management'),
   
]