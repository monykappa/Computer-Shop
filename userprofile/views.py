from multiprocessing import AuthenticationError

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.views.generic import ListView
from products.models import *
from django.shortcuts import render, get_object_or_404
from orders.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse


# Create your views here.

class SignInView(View):
    def get(self, request):
        return render(request, "auth/sign_in.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})


def signup(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    if request.method == "POST":
        full_name = request.POST["full_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        pfp = request.FILES.get("pfp")

        first_name, last_name = (
            full_name.split(" ", 1) if " " in full_name else (full_name, "")
        )

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        else:
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, "Username is already taken. Please choose a different one."
                )
            elif User.objects.filter(email=email).exists():
                messages.error(
                    request,
                    "Email is already registered. Please use a different email address.",
                )
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                )

                # Create UserProfile instance and associate it with the user
                UserProfile.objects.create(user=user, pfp=pfp)

                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user)
                messages.success(request, "Account created successfully.")
                return redirect("home:home_auth")

    return render(request, "auth/sign_up.html")


def check_username_availability(request):
    username = request.GET.get("username")
    data = {
        "is_taken": User.objects.filter(username=username).exists(),
        "message": (
            "Username is already taken. Please choose a different one."
            if User.objects.filter(username=username).exists()
            else ""
        ),
    }
    return JsonResponse(data)


def check_email_availability(request):
    email = request.GET.get("email")
    data = {
        "is_taken": User.objects.filter(email=email).exists(),
        "message": (
            "Email is already registered. Please use a different email address."
            if User.objects.filter(email=email).exists()
            else ""
        ),
    }
    return JsonResponse(data)

class MyInfoView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/my_info.html'

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home:home")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile.html"

class EditUsernameView(UpdateView):
    model = User
    fields = ['username']
    template_name = 'edit/edit_username.html'
    success_url = reverse_lazy('userprofile:my_info')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'username': self.object.username})
        return response

class EditFullNameView(UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    template_name = 'edit/edit_full_name.html'
    success_url = reverse_lazy('userprofile:my_info')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'full_name': self.object.get_full_name()})
        return response


class EditAddressView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'edit/edit_address.html'
    success_url = reverse_lazy('userprofile:my_info')

    def get_object(self):
        return Address.objects.get_or_create(user=self.request.user)[0]

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {
                'address1': self.object.address1,
                'address2': self.object.address2,
                'city': self.object.city,
                'province': self.object.province,
                'phone': self.object.phone,
            }
            return JsonResponse(data)
        return response

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)