from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('schedule/', views.staff_schedule, name='staff_schedule'),
    path('create-schedule/', views.create_schedule, name='create_schedule'),
    path('manager-schedule/', views.manager_schedule, name='manager_schedule'),
    path("staff-schedule/", views.staff_schedule, name="staff_schedule"),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('view-schedules/', views.view_schedules, name='view_schedules'),
    path("logout/", auth_views.LogoutView.as_view(next_page='/'), name="logout"),  # Redirects to homepage after logout
    
]

