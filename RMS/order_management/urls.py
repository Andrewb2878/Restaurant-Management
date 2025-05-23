from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from .views import order_management, view_order_items  # Import the function

urlpatterns = [
    path('order-management/', views.order_management, name='order_management'),
    path('view-order-items/<int:order_id>/', view_order_items, name='view_order_items'),
    path("update-order-status/<int:order_id>/", views.update_order_status, name="update_order_status"),
    path('get-total-orders/', views.get_total_orders, name='get_total_orders'), 
    path('get-total-revenue/', views.get_total_revenue, name='get_total_revenue'),  


]
