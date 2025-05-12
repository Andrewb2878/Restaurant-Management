"""
URL configuration for RMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import index, menu, feedback, portal
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('menu/', menu, name='menu'),
    path('reservation/', include('reservation.urls')),
    path('feedback/', feedback, name='feedback'),
    path('portal/', portal, name='portal'),
    path('staff-scheduling/', include('staff_scheduling.urls')),  # Link to staff scheduling app
    path('core/', include('core.urls')),  # Staff URL links (dashboards and view feedback form)
    path('order-management/', include('order_management.urls')),  # Link to order management app
    path('order-management/', include(('order_management.urls', 'order_management'), namespace='order_management')),  # Link to order management app
    path('inventory/', include('inventory.urls')),  # Link to inventory app

]

# Serve media files during development
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

