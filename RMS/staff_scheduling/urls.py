from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.staff_schedule, name='staff_schedule'),
    path('create-schedule/', views.create_schedule, name='create_schedule'),
    path('manager-view/', views.manager_schedule, name='manager_schedule'),
    path('test-template/', views.test_template, name='test_template'),
]