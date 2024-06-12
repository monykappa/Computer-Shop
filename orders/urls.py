from django.urls import path, include
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings

app_name = 'orders'

urlpatterns = [
    path('check-login-status/', views.CheckLoginStatusView.as_view(), name='check_login_status'),
    path('add-to-cart/<slug:slug>/',views. AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('clear-cart/', views.ClearCartView.as_view(), name='clear_cart'),
    path('cart/remove/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/update_cart_quantity/<int:item_id>/', views.UpdateCartQuantityView.as_view(), name='update_cart_quantity'),
    path('payment_complete/', views.PaymentCompleteView.as_view(), name='payment_complete'),
    
    
    path('order-history-image/<int:order_history_id>/', views.OrderHistoryImageView.as_view(), name='order_history_image'),

    
    path('order-history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('order-history/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    # path('save-address/', views.SaveAddressView.as_view(), name='save_address'),  # Define the URL pattern for save_address
    # path('confirm-address/', views.ConfirmAddressView.as_view(), name='confirm_address'),
    path('confirm-address/', views.confirm_address, name='confirm_address'),
    path('pay-with-paypal/', views.pay_with_paypal, name='pay_with_paypal'),
    
    path('paypal/', include('paypal.standard.ipn.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

