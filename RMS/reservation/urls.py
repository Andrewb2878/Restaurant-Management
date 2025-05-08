from django.urls import path
from . import views

urlpatterns = [
    path('reservation', views.reservation, name='reservation'),
    path('view_reservations', views.view_reservations, name='view_reservations')
]
