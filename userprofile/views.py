
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

# Create your views here.

# create sign in view for me 
class SignInView(View):
    def get(self, request):
        return render(request, 'auth/sign_in.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home:home_auth')
        else:
            return redirect(f"{reverse('userprofile:sign_in')}?error=1")
        


def signup(request):
    if request.user.is_authenticated:
        return redirect('home:home')  
    if request.method == 'POST':
        full_name = request.POST['full_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        pfp = request.FILES.get('pfp')

        first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken. Please choose a different one.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered. Please use a different email address.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1,
                                                first_name=first_name, last_name=last_name)

                # Create UserProfile instance and associate it with the user
                UserProfile.objects.create(user=user, pfp=pfp)

                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                messages.success(request, "Account created successfully.")
                return redirect('home:home_auth')

    return render(request, 'auth/sign_up.html')


def check_username_availability(request):
    username = request.GET.get('username')
    data = {
        'is_taken': User.objects.filter(username=username).exists(),
        'message': 'Username is already taken. Please choose a different one.' if User.objects.filter(username=username).exists() else ''
    }
    return JsonResponse(data)

def check_email_availability(request):
    email = request.GET.get('email')
    data = {
        'is_taken': User.objects.filter(email=email).exists(),
        'message': 'Email is already registered. Please use a different email address.' if User.objects.filter(email=email).exists() else ''
    }
    return JsonResponse(data)


    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:home')



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'