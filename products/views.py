from shared_imports import *

class ProductListView(TemplateView):
    template_name = 'products/products.html'

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

class RelatedProductsView(ListView):
    model = LaptopSpec
    template_name = 'products/related_products.html'
    context_object_name = 'related_products'
    paginate_by = 10  # Number of products per page

    def get_queryset(self):
        current_laptop = LaptopSpec.objects.get(slug=self.kwargs['slug'])
        brand_name = current_laptop.product.brand.name  # Assuming 'brand' is a related field in your LaptopSpec model

        related_products = LaptopSpec.objects.filter(product__brand__name=brand_name).exclude(slug=self.kwargs['slug'])
        return related_products

class PublicLaptopSpecListAPIView(generics.ListAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer
    permission_classes = []  # No special permissions needed

class PublicBrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = []  # No special permissions needed

class LaptopSpecListAPIView(generics.ListAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer
    permission_classes = [IsSuperAdmin]  # Apply the custom permission

class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsSuperAdmin]  # Apply the custom permission

class LaptopSpecDetailAPIView(generics.RetrieveAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer
    lookup_field = 'slug'
    permission_classes = [IsSuperAdmin]  # Apply the custom permission

class PublicLaptopSpecDetailAPIView(generics.RetrieveAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer
    lookup_field = 'slug'
    permission_classes = []  # No special permissions needed

class RecommendedProductsAPIView(APIView):
    permission_classes = [IsSuperAdmin]  # Apply the custom permission

    def get(self, request, slug):
        all_laptops = list(LaptopSpec.objects.exclude(slug=slug))
        if len(all_laptops) > 5:
            recommended_products = random.sample(all_laptops, 5)
        else:
            recommended_products = all_laptops

        serializer = LaptopSpecSerializer(recommended_products, many=True)
        return Response(serializer.data)

class PublicRecommendedProductsAPIView(APIView):
    permission_classes = []  # No special permissions needed

    def get(self, request, slug):
        all_laptops = list(LaptopSpec.objects.exclude(slug=slug))
        if len(all_laptops) > 5:
            recommended_products = random.sample(all_laptops, 5)
        else:
            recommended_products = all_laptops

        serializer = LaptopSpecSerializer(recommended_products, many=True)
        return Response(serializer.data)
