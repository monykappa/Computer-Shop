from shared_imports import *


def compare(request):
    search_query = request.GET.get('search', '')

    products = Product.objects.filter(name__icontains=search_query).prefetch_related(
        Prefetch('images', queryset=ProductImage.objects.all().order_by('id')[:1], to_attr='first_image')
    ) if search_query else Product.objects.none()

    if 'compared_products' not in request.session:
        request.session['compared_products'] = []

    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')

        if action == 'add' and product_id:
            if product_id not in request.session['compared_products'] and len(request.session['compared_products']) < 3:
                request.session['compared_products'].append(product_id)
                request.session.modified = True
        elif action == 'remove' and product_id:
            if product_id in request.session['compared_products']:
                request.session['compared_products'].remove(product_id)
                request.session.modified = True
        elif action == 'clear':
            request.session['compared_products'] = []
            request.session.modified = True

    compared_products = Product.objects.filter(id__in=request.session['compared_products']).prefetch_related(
        Prefetch('images', queryset=ProductImage.objects.all().order_by('id')[:1], to_attr='first_image')
    )

    max_compare_limit_reached = len(request.session['compared_products']) >= 3
    context = {
            'search_query': search_query,
            'products': products,
            'compared_products': compared_products,
            'max_compare_limit_reached': max_compare_limit_reached
        }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # If it's an AJAX request, return only the product list
            html = render_to_string('home/partials/product_list.html', context, request=request)
            return HttpResponse(html)
        
    return render(request, 'home/compare.html', context)

    
class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Most ordered items
        most_ordered_items = OrderHistoryItem.objects.values('product_id').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:8]
        most_ordered_ids = [item['product_id'] for item in most_ordered_items]
        
        # Newest products
        newest_products = Product.objects.order_by('-id')[:8]  # Using 'id' as a proxy for creation time
        
        # Affordable products
        affordable_products = Product.objects.order_by('price')[:8]
        
        # Combine and prefetch related data
        product_ids = list(set(most_ordered_ids + list(newest_products.values_list('id', flat=True)) + list(affordable_products.values_list('id', flat=True))))
        products = Product.objects.filter(id__in=product_ids).prefetch_related(
            'images',
            Prefetch('laptop_spec', queryset=LaptopSpec.objects.select_related('cpu__cpu_brand', 'storage', 'memory').prefetch_related('gpu__gpu_brand'))
        ).select_related('color')
        
        # Sort most ordered products
        most_ordered_products = sorted([p for p in products if p.id in most_ordered_ids], key=lambda x: most_ordered_ids.index(x.id))
        
        context['most_ordered_items'] = most_ordered_products[:8]
        context['newest_products'] = newest_products[:8]
        context['affordable_products'] = affordable_products
        return context
    
    
# If user is logged in, show home_auth.html
class HomeAuth(LoginRequiredMixin, TemplateView):
    def get(self, request):
        template = 'home/home_auth.html'
        return render(request, template)
    

class AboutUsAPIView(APIView):
    def get(self, request):
        about_content = AboutUs.objects.first()
        if about_content:
            serializer = AboutUsSerializer(about_content)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

def about_us(request):
    return render(request, 'home/about_us.html')


class ContactUsAPIView(APIView):
    def get(self, request):
        contact_content = ContactUs.objects.first()
        if contact_content:
            serializer = ContactUsSerializer(contact_content)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

def contact(request):
    return render(request, 'home/contact.html')

class NotificationView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'profile/notifications.html'
    context_object_name = 'notifications'
    login_url = reverse_lazy('userprofile:sign_in')
    paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

@login_required
@require_POST
@csrf_protect
def mark_notification_as_read(request):
    notification_id = request.POST.get('notification_id')
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    

@login_required
@require_POST
@csrf_protect
def mark_all_notifications_as_read(request):
    try:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


