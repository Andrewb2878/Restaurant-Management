from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('inventory/', views.inventory, name='inventory'),
    path('place-order/', views.place_order, name='place_order'),
    path('update-inventory/', views.update_inventory, name='update_inventory'),
    path('add-item/', views.add_item, name='add_item'),

]