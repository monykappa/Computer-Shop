from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Advertise)
class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    