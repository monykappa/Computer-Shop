from django.urls import path, include
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings

app_name = 'delivery'

urlpatterns = [
    path('dashboard/delivery/', views.delivery_guy_dashboard, name='delivery_guy_dashboard'),
    path('complete/<int:assignment_id>/', views.mark_delivery_complete, name='mark_delivery_complete'),
    path('create/', views.create_delivery_staff, name='create_delivery_staff'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

