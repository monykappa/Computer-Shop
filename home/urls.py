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
    # path('api/products/', views.ProductSearchView.as_view(), name='product-search'),
    # path('api/public-products/', views.PublicProductSearchView.as_view(), name='public-product-search'),


    path('api/about-us/', views.AboutUsAPIView.as_view(), name='about_us_api'),
    path('about-us/', views.about_us, name='about-us'),
    
    path('api/contact-us/', views.ContactUsAPIView.as_view(), name='contact_us_api'),
    path('contact/', views.contact, name='contact'),
    
    path('notifications/', views.NotificationView.as_view(), name='notifications'),
    path('mark-notification-as-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark-all-notifications-as-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    
    
    path('compare/', views.compare, name='compare'),
    
    path('rate-product/<int:item_id>/', views.RateProductView.as_view(), name='rate_product'),
    
    
    
    # path('most-ordered-product/', views.most_ordered_product, name='most_ordered_product'),
    # authentication

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
