from django.urls import path
from .views import MySuperAdminView

urlpatterns = [
    path('superadmin/', MySuperAdminView.as_view(), name='superadmin'),
]
