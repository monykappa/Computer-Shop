from django.db import models

# Create your models here.
class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='advertisements/images/')
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0, help_text="Higher priority ads will be shown first")

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.title