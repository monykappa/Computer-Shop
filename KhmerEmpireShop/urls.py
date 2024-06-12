
from django.contrib import admin
from django.urls import path

from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('products.urls')),
    path('', include('userprofile.urls')),
    path('', include('orders.urls')),
    path('', include('dashboard.urls')),
    
    
    
    
    path('accounts/', include('allauth.urls')),
    
    
]
