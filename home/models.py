# import
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField # type: ignore
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
        

class ContactUs(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    map_embed = models.TextField(blank=True, null=True)  # For Google Maps embed code
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Contact Us"
        
class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "About Us"


from django.db import models

class Footer(models.Model):
    phone_number = models.CharField(max_length=20)
    copyright_text = models.CharField(max_length=200)

    def __str__(self):
        return "Footer Information"

    class Meta:
        verbose_name_plural = "Footer"

class SocialMedia(models.Model):
    footer = models.ForeignKey(Footer, on_delete=models.CASCADE, related_name='social_media')
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon_class = models.CharField(max_length=50, help_text="Font Awesome icon class")

    def __str__(self):
        return f"{self.platform} for {self.footer}"

    class Meta:
        verbose_name_plural = "Social Media Links"