from django.urls import path, include
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.shortcuts import render
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = "userprofile"

urlpatterns = [
    # Authentication
    path("sign-in/", views.SignInView.as_view(), name="sign_in"),
    path("signup/", views.signup, name="signup"),
    path(
        "check-username/",
        views.check_username_availability,
        name="check_username_availability",
    ),
    path(
        "check-email/", views.check_email_availability, name="check_email_availability"
    ),
    
    path('edit-username/', views.EditUsernameView.as_view(), name='edit_username'),
    path('edit-full-name/', views.EditFullNameView.as_view(), name='edit_full_name'),
    path('edit-address/', views.EditAddressView.as_view(), name='edit_address'),
    
    # logout
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # Profile
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path('my_info/', views.MyInfoView.as_view(), name='my_info'),
    # api
    # path('api/profile/', views.ProfileAPIView.as_view(), name='profile-api'),
    # Password reset
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
