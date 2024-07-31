from django.urls import path, include
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render 
from . import views
from django.conf import settings

app_name = 'dashboard'

urlpatterns = [
    # path('base/', views.base, name='base'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/sign_in/', views.DashboardSignInView.as_view(), name='sign_in'),
    path('dashboard/logout/', views.DashboardLogoutView.as_view(), name='logout'),
    
    
    path('dashboard/order/', views.OrderHistoryView.as_view(), name='order'),
    path('dashboard/order/<int:pk>/update_status/', views.OrderStatusUpdateView.as_view(), name='order_status_update'),

    path('advertisements/', views.AdvertisementListView.as_view(), name='advertisement_list'),
    path('advertisements/create/', views.AdvertisementCreateView.as_view(), name='advertisement_create'),
    path('advertisements/<int:pk>/edit/', views.AdvertisementUpdateView.as_view(), name='advertisement_edit'),
    path('dashboard/advertisements/<int:pk>/delete/', views.AdvertisementDeleteView.as_view(), name='advertisement_delete'),

    
    path('dashboard/products/', views.ProductListView.as_view(), name='product_list'),
    path('dashboard/products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('delete-product-image/<int:pk>/', views.ProductImageDeleteView.as_view(), name='delete_product_image'),
    # path('delete-product-image/<int:image_id>/', views.DeleteProductImageView.as_view(), name='delete_product_image'),
    
    path('dashboard/order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    
    path('stocks/', views.StockListView.as_view(), name='stock_list'),
    path('stock/add/', views.add_stock, name='add_stock'),
    path('stock/<int:pk>/edit/', views.StockUpdateView.as_view(), name='stock_edit'),
    path('check-stock-exists/', views.check_stock_exists, name='check_stock_exists'),
    
    path('dashboard/tables/', views.DisplayTablesView.as_view(), name='display_tables'),
    path('dashboard/<str:model_name>/create/', views.GenericModelFormView.as_view(), name='model_create'),
    path('delete/<str:model_name>/<int:pk>/', views.GenericDeleteView.as_view(), name='model_delete'),
    # path('<str:model_name>/<int:pk>/update/', views.GenericModelFormView.as_view(), name='model_update'),
    path('dashboard/edit/<str:model>/<int:pk>/', views.EditModelView.as_view(), name='edit_model'),
    
    
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('staff/update/<int:pk>/', views.DeliveryStaffUpdateView.as_view(), name='staff_update'),
    path('users/add/', views.AddSuperuserView.as_view(), name='add_superuser'),
    
    
    path('dashboard/create/', views.DeliveryStaffCreateView.as_view(), name='create_delivery_staff'),   
    
    
    path('dashboard/assign/', views.AssignOrderView.as_view(), name='assign_order'),
    path('dashboard/assign-order-history/', views.AssignOrderHistoryListView.as_view(), name='assign_order_history'),
    
    
    path('mark_order_as_read/', views.mark_order_as_read, name='mark_order_as_read'),
    
    
    path('dashboard/charts/', views.OrdersByDateChartsView.as_view(), name='orders_by_date_charts'),
    path('dashboard/users-charts/', views.UsersChartsView.as_view(), name='users_charts'),
    path('dashboard/revenue-chart/', views.RevenueByDateChartView.as_view(), name='revenue_by_period'),
    path('top-products-by-date/', views.TopProductsChartView.as_view(), name='top_products_chart'),


    path('api/products/all', views.AllProductsAPI.as_view(), name='all_products_api'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

