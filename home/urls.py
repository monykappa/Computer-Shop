from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static
from home import views



app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('base/', BaseView.as_view(), name='base'),
    path('', HomeAuth.as_view(), name='home_auth'),
    path('api/products/', views.ProductSearchView.as_view(), name='product-search'),


    path('api/about-us/', views.AboutUsAPIView.as_view(), name='about_us_api'),
    path('about-us/', views.about_us, name='about-us'),
    
    path('api/contact-us/', views.ContactUsAPIView.as_view(), name='contact_us_api'),
    path('contact/', views.contact, name='contact'),
    # authentication

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
