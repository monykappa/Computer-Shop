# In a new file called serializers.py in your app directory
from rest_framework import serializers # type: ignore
from .models import *

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['title', 'content', 'last_updated']

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['title', 'content', 'email', 'phone', 'address', 'map_embed', 'last_updated']