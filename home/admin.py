from django.contrib import admin
from .models import *

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url_name', 'url_name_auth', 'order', 'authenticated_only')
    ordering = ('order',)

admin.site.register(MenuItem, MenuItemAdmin)
# admin.site.register(SocialMediaLink)
