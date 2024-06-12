
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
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView


# If user is not logged in, show home.html
class HomeView(TemplateView):
    template_name = 'home/home.html'

# class BaseView(LoginRequiredMixin, TemplateView):
#     template_name = 'base.html'

# If user is logged in, show home_auth.html
class HomeAuth(LoginRequiredMixin, TemplateView):
    def get(self, request):
        template = 'home/home_auth.html'
        return render(request, template)
    







