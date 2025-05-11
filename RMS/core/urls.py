from django.urls import path
from . import views


urlpatterns = [
    path('chef-dashboard/', views.chef_dashboard, name='chef_dashboard'),
    path('waiter-dashboard/', views.waiter_dashboard, name='waiter_dashboard'),
    path('view-feedback/', views.view_feedback, name='view_feedback'),
    path('feedback/toggle-read/<int:feedback_id>/', views.toggle_feedback_read, name='toggle_feedback_read'),
    path('feedback/delete/<int:pk>/', views.delete_feedback, name='delete_feedback'),
    
 
    
]

