from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
import random
from .serializers import *
from rest_framework import generics
from django.views.generic import TemplateView




class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class LaptopSpecListAPIView(generics.ListAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer

class ProductListView(TemplateView):
    template_name = 'products/products.html'

class LaptopSpecDetailAPIView(generics.RetrieveAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer
    lookup_field = 'slug'
    
class ProductDetailView(DetailView):
    model = LaptopSpec
    template_name = 'products/products_detail.html'
    context_object_name = 'laptop_spec'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['laptop_slug'] = self.kwargs['slug']
        return context
    
    def get_random_recommendations(self):
        all_laptops = list(LaptopSpec.objects.exclude(slug=self.kwargs['slug']))
        if len(all_laptops) > 5:
            recommended_products = random.sample(all_laptops, 5)
        else:
            recommended_products = random.sample(all_laptops, len(all_laptops))
        return recommended_products

class RelatedProductsView(ListView):
    model = LaptopSpec
    template_name = 'products/related_products.html'
    context_object_name = 'related_products'
    paginate_by = 10  # Number of products per page

    def get_queryset(self):
        current_laptop = LaptopSpec.objects.get(slug=self.kwargs['slug'])
        brand_name = current_laptop.brand_name  # Assuming 'brand_name' is an attribute in your LaptopSpec model

        related_products = LaptopSpec.objects.filter(brand_name=brand_name).exclude(slug=self.kwargs['slug'])
        return related_products
