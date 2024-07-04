from django.contrib import admin
from .models import *
from django import forms
from ckeditor.widgets import CKEditorWidget

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url_name', 'url_name_auth', 'order', 'authenticated_only')
    ordering = ('order',)
    
class AboutUsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = AboutUs
        fields = '__all__'

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    form = AboutUsAdminForm
    list_display = ('title', 'last_updated')
    search_fields = ('title', 'content')
    readonly_fields = ('last_updated',)

    fieldsets = (
        (None, {
            'fields': ('title', 'content')
        }),
        ('Metadata', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return AboutUs.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        return False
    

class ContactUsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = ContactUs
        fields = '__all__'

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    form = ContactUsAdminForm
    list_display = ('title', 'email', 'phone', 'last_updated')
    search_fields = ('title', 'content', 'email', 'phone', 'address')
    readonly_fields = ('last_updated',)

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'email', 'phone', 'address', 'map_embed')
        }),
        ('Metadata', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return ContactUs.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        return False
    
    
    
admin.site.register(MenuItem, MenuItemAdmin)

# admin.site.register(SocialMediaLink)
