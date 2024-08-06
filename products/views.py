    
from shared_imports import *


class ProductListView(ListView):
    model = LaptopSpec
    template_name = 'products/products.html'
    context_object_name = 'laptop_specs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        laptop_specs = self.get_queryset()
        context['laptop_specs'] = laptop_specs
        return context

def search_products(request):
    query = request.GET.get('q', '')
    if query:
        try:
            # Filter products
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(model__icontains=query) |
                Q(brand__name__icontains=query)
            ).prefetch_related('images').values(
                'id', 'name', 'model', 'brand__name', 'price', 'year'
            )

            # Convert queryset to list and add image URLs and LaptopSpec slugs
            product_list = list(products)
            base_url = settings.MEDIA_URL

            for product in product_list:
                product_instance = Product.objects.get(id=product['id'])
                product['images'] = [
                    {'image': image.image.url} for image in product_instance.images.all()
                ]

                # Get the corresponding LaptopSpec slug
                laptop_spec = LaptopSpec.objects.filter(product=product_instance).first()
                if laptop_spec:
                    product['slug'] = laptop_spec.slug

            return JsonResponse(product_list, safe=False)
        except Exception as e:
            logger.error(f"Error in search_products: {str(e)}", exc_info=True)
            return JsonResponse({'error': 'Internal server error'}, status=500)
    return JsonResponse([], safe=False)



class ProductDetailView(DetailView):
    model = LaptopSpec
    template_name = 'products/products_detail.html'
    context_object_name = 'laptop_spec'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_laptop = self.object
        brand_name = current_laptop.product.brand.name
        
        # Get related products
        related_products = LaptopSpec.objects.filter(product__brand__name=brand_name).exclude(slug=self.kwargs['slug'])[:10]
        context['related_products'] = related_products
        
        # Get top-selling products
        most_ordered_items = OrderHistoryItem.objects.values('product_id').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:8]
        most_ordered_ids = [item['product_id'] for item in most_ordered_items]
        top_selling_products = LaptopSpec.objects.filter(id__in=most_ordered_ids)
        context['top_selling_products'] = top_selling_products
        
        return context


        
class PublicLaptopSpecListAPIView(generics.ListAPIView):
    queryset = LaptopSpec.objects.all()
    serializer_class = LaptopSpecSerializer
    permission_classes = []


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
