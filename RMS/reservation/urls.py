from django.urls import path
from . import views

urlpatterns = [
    path('reservation', views.reservation, name='reservation'),
    path('view-reservations', views.view_reservations, name='view_reservations'),
    path('delete/<int:id>/', views.delete_reservation, name='delete_reservation'),
    path('cancel/<int:id>/', views.cancel_reservation, name='cancel_reservation'),
]
