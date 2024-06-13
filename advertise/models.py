from django.db import models
from django.core.exceptions import ValidationError
import os 
from django.utils.safestring import mark_safe

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    
# Create your models here.
class Advertise(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='ads/', validators=[validate_file_extension])
    link = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(self.image.url))
        else:
            return '(No image)'

    image_tag.short_description = 'Image'