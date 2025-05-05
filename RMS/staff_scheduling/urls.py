from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.staff_schedule, name='staff_schedule'),
    path('create-schedule/', views.create_schedule, name='create_schedule'),
    path('manager-schedule/', views.manager_schedule, name='manager_schedule'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
]

