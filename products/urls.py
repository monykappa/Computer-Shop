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
    path('api/public-brands/', views.PublicBrandListAPIView.as_view(), name='public-brand-list'),
    path('api/laptop-specs/', views.LaptopSpecListAPIView.as_view(), name='laptop-spec-list'),
    path('api/public-laptop-specs/', views.PublicLaptopSpecListAPIView.as_view(), name='public-laptop-spec-list'),
    # path('api/laptop-specs/<slug:slug>/', views.LaptopSpecDetailAPIView.as_view(), name='laptop-spec-detail'),
    path('api/public-laptop-specs/<slug:slug>/', views.PublicLaptopSpecDetailAPIView.as_view(), name='public-laptop-spec-detail'),
    path('api/recommended-products/<slug:slug>/', views.RecommendedProductsAPIView.as_view(), name='recommended-products'),
    path('api/public-recommended-products/<slug:slug>/', views.PublicRecommendedProductsAPIView.as_view(), name='public-recommended-products'),
    
    path('search/', views.search_products, name='search_products'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

