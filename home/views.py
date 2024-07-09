
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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from products.serializers import *
from .serializers import *
from .models import *




# class ProductSearchView(APIView):
#     pagination_class = LimitOffsetPagination  # Define pagination class here
#     filter_backends = [SearchFilter]
#     search_fields = ['name', 'description']

#     def get(self, request):
#         try:
#             queryset = Product.objects.all()
#             query = self.request.query_params.get('q', None)
#             if query:
#                 queryset = queryset.filter(name__icontains=query)
#             # Paginate queryset
#             page = self.pagination_class().paginate_queryset(queryset, request)
#             if page is not None:
#                 serializer = ProductSerializer(page, many=True)
#                 return self.pagination_class().get_paginated_response(serializer.data)
#             else:
#                 serializer = ProductSerializer(queryset, many=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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