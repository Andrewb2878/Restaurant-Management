from django.urls import path
from . import views

urlpatterns = [
    path('chef-dashboard/', views.chef_dashboard, name='chef_dashboard'),
    path('waiter-dashboard/', views.waiter_dashboard, name='waiter_dashboard'),
]