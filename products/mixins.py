from django.db import models
from django.utils.text import slugify

class SlugMixin(models.Model):
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        abstract = True

    def generate_unique_slug(self):
        slug = slugify(self.slug_source)
        unique_slug = slug
        num = 1
        ModelClass = self.__class__

        while ModelClass.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1

        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    @property
    def slug_source(self):
        raise NotImplementedError("Subclasses must define the slug_source property.")
