from django.urls import path, include
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings

app_name = 'products'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('api/brands/', views.BrandListAPIView.as_view(), name='brand-list'),
    path('api/laptop-specs/', views.LaptopSpecListAPIView.as_view(), name='laptop-spec-list'),
    path('api/laptop-specs/<slug:slug>/', views.LaptopSpecDetailAPIView.as_view(), name='laptop-spec-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

