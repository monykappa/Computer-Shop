from django.shortcuts import render
# import
from rest_framework import generics
from .models import *
from .serializers import AdvertisementSerializer


# Create your views here.
class AdvertisementViewSet(generics.ListAPIView):
    queryset = Advertisement.objects.all().order_by('-priority', '-created_at')
    serializer_class = AdvertisementSerializer