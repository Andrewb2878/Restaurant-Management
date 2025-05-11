from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from .views import order_management, view_order_items  # Import the function

urlpatterns = [
    path('order-management/', views.order_management, name='order_management'),
    path('view-order-items/<int:order_id>/', view_order_items, name='view_order_items'),
   
]

