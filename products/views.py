from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404




class ProductListView(ListView):
    model = LaptopSpec
    template_name = 'products/products.html'
    context_object_name = 'laptop_specs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all laptop brands
        context['laptop_brands'] = Brand.objects.all()
        return context

class ProductDetailView(DetailView):
    model = LaptopSpec
    template_name = 'products/products_detail.html'
    context_object_name = 'laptop_spec'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

