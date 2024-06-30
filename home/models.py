# import
from django.db import models
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch




class MenuItem(models.Model):
    name = models.CharField(max_length=100, blank=True)
    url_name = models.CharField(max_length=100, help_text="The name of the URL pattern for unauthenticated users")
    url_name_auth = models.CharField(max_length=100, blank=True, null=True, help_text="The name of the URL pattern for authenticated users")
    order = models.IntegerField(default=0)
    icon = models.CharField(max_length=100, blank=True, null=True)
    authenticated_only = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_url(self, user):
        try:
            if user.is_authenticated and self.url_name_auth:
                return reverse(self.url_name_auth)
            return reverse(self.url_name)
        except NoReverseMatch:
            return '#'
        
# class SocialMediaLink(models.Model):
#     platform_name = models.CharField(max_length=50)
#     url = models.URLField()
#     icon = models.CharField(max_length=50, blank=True, null=True, help_text='FontAwesome icon class')

#     def __str__(self):
#         return self.platform_name

    