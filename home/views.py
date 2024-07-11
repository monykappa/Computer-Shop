
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
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.pagination import LimitOffsetPagination # type: ignore
from rest_framework.filters import SearchFilter # type: ignore
from products.serializers import *
from .serializers import *
from .models import *
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy






    
# If user is not logged in, show home.html
class HomeView(TemplateView):
    template_name = 'home/home.html'

# If user is logged in, show home_auth.html
class HomeAuth(LoginRequiredMixin, TemplateView):
    def get(self, request):
        template = 'home/home_auth.html'
        return render(request, template)
    

class AboutUsAPIView(APIView):
    def get(self, request):
        about_content = AboutUs.objects.first()
        if about_content:
            serializer = AboutUsSerializer(about_content)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

def about_us(request):
    return render(request, 'home/about_us.html')


class ContactUsAPIView(APIView):
    def get(self, request):
        contact_content = ContactUs.objects.first()
        if contact_content:
            serializer = ContactUsSerializer(contact_content)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

def contact(request):
    return render(request, 'home/contact.html')

class NotificationView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'profile/notifications.html'
    context_object_name = 'notifications'
    login_url = reverse_lazy('userprofile:sign_in')

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

@login_required
@require_POST
@csrf_protect
def mark_notification_as_read(request):
    notification_id = request.POST.get('notification_id')
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    

@login_required
@require_POST
@csrf_protect
def mark_all_notifications_as_read(request):
    try:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
