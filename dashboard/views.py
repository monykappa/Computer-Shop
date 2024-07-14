import json
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout
from products.models import *
from orders.models import *
from datetime import date, timedelta
from django.views.generic import ListView, DetailView
from .mixins import SuperuserRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
import io
from bokeh.plotting import figure # type: ignore
from bokeh.embed import components # type: ignore
from plotly.offline import plot # type: ignore
import plotly.graph_objs as go # type: ignore
from userprofile.models import *
from .forms import *
from advertisements.forms import * 
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from delivery.models import *
from delivery.forms import *
from django.views.generic import FormView, ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from delivery.forms import *
from django.db.models import Prefetch
from advertisements.models import *
# import
from django.db.models import Prefetch
from django.db import transaction
import datetime
# import q
from django.db.models import Q
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt



class DashboardView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    login_url = reverse_lazy('dashboard:sign_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Total number of products
        context['total_products'] = Product.objects.count()
        
        # Total number of orders
        context['total_orders'] = OrderHistory.objects.count()
        
        # Total number of users
        context['total_users'] = User.objects.count()

        # Retrieve the newest product
        newest_product = Product.objects.latest('id')
        context['newest_product_name'] = newest_product.name

        # Count pending orders
        context['pending_orders'] = OrderHistory.objects.filter(status=OrderStatus.PENDING).count()

        # Count orders assigned to delivery (exclude completed deliveries)
        context['assigned_to_delivery'] = DeliveryAssignment.objects.filter(completed_at__isnull=True).count()

        # Get top 5 most ordered products with their models and year
        top_products = OrderHistoryItem.objects.values('product__name', 'product__model', 'product__description', 'product__year').annotate(total_ordered=Sum('quantity')).order_by('-total_ordered')[:5]

        product_info = [f"{item['product__name']} - {item['product__model']} - {item['product__description']} ({item['product__year']})" for item in top_products]
        quantities = [item['total_ordered'] for item in top_products]

        # Create Plotly bar chart for top products with different colors
        colors = ['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD']  # Example colors
        data = [
            go.Bar(
                x=product_info,
                y=quantities,
                marker=dict(color=colors),
                hoverinfo='text',
                text=product_info,
                textposition='auto'
            )
        ]

        layout = go.Layout(
            title='Top 5 Most Ordered Products',
            yaxis=dict(title='Quantity Ordered'),
            xaxis=dict(title='Product Information'),
            margin=dict(b=150)  # Adjust bottom margin to accommodate longer product names
        )

        chart = plot({'data': data, 'layout': layout}, output_type='div', include_plotlyjs=False)

        # Indent text under the chart due to its length
        text_under_chart = """
            This bar chart displays the top 5 most ordered products with their models and years. 
            Each bar represents the quantity ordered for each product.
            """

        context['chart'] = chart
        context['text_under_chart'] = text_under_chart

        # Bar chart for user distribution
        user_counts = User.objects.aggregate(
            super_admin_count=Count('id', filter=Q(is_superuser=True)),
            customer_user_count=Count('id', filter=Q(is_superuser=False, deliverystaff__isnull=True)),
            delivery_staff_count=Count('deliverystaff')
        )

        user_data = [
            go.Bar(
                x=['Super Admin', 'Customer User', 'Delivery Staff'],
                y=[user_counts['super_admin_count'], user_counts['customer_user_count'], user_counts['delivery_staff_count']],
                marker=dict(color=['#FF9999', '#66B2FF', '#99FF99'])
            )
        ]

        user_layout = go.Layout(
            title='User Distribution',
            yaxis=dict(title='Number of Users')
        )

        user_chart = plot({'data': user_data, 'layout': user_layout}, output_type='div', include_plotlyjs=False)

        context['user_chart'] = user_chart

        return context
    
    
class DashboardSignInView(LoginView):
    template_name = 'dashboard/sign_in.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return JsonResponse({
            'success': True,
            'redirect_url': self.get_success_url()
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'message': 'Invalid username or password.'
        }, status=400)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'deliverystaff'): 
                return reverse_lazy('delivery:delivery_guy_dashboard')
            else:
                return reverse_lazy('dashboard:dashboard')
        return reverse_lazy('dashboard:login')
    
    
class DashboardLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('dashboard:sign_in')


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'dashboard/ads/advertisement_list.html'
    context_object_name = 'advertisements'
    ordering = ['-priority', '-created_at']
    paginate_by = 10  # Show 10 ads per page
    


class AdvertisementCreateView(CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'dashboard/ads/advertisement_create.html'  # Create this template
    success_url = reverse_lazy('dashboard:advertisement_list')
    
    
class AdvertisementUpdateView(SuccessMessageMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'dashboard/ads/advertisement_form.html'
    success_url = reverse_lazy('dashboard:advertisement_list')
    success_message = "Advertisement updated successfully!"

@method_decorator(csrf_exempt, name='dispatch')
class AdvertisementDeleteView(DeleteView):
    model = Advertisement
    success_url = reverse_lazy('dashboard:advertisement_list')

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    
    

class OrderHistoryView(SuperuserRequiredMixin, LoginRequiredMixin, ListView):
    model = OrderHistory
    template_name = 'dashboard/orders.html'
    context_object_name = 'order_histories'
    paginate_by = 10  

    def get_queryset(self):
        # Filter the order history by status
        status = self.request.GET.get('status', OrderStatus.PENDING)
        queryset = OrderHistory.objects.filter(status=status).order_by('-ordered_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', OrderStatus.PENDING)
        
        # Add address data for each order
        for order in context['order_histories']:
            address = Address.objects.filter(user=order.user).first()
            if address:
                order.province = address.province
            else:
                order.province = 'N/A'
                
        return context

class OrderStatusUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, View):
    def post(self, request, pk):
        order_history = get_object_or_404(OrderHistory, pk=pk)
        new_status = request.POST.get('status')
        if new_status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            order_history.update_status(new_status)
            
            # Create a notification for the user
            notification_message = f'Your order #{order_history.id} has been {new_status.lower()}.'
            Notification.objects.create(
                user=order_history.user,
                message=notification_message,
                created_at=timezone.now(),
                is_read=False
            )
            
            messages.success(request, f'Order {order_history.id} has been updated to {new_status}')
        else:
            messages.error(request, 'Invalid status')
        return redirect('dashboard:order')


class OrderDetailView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    model = OrderHistory
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'order'
    login_url = reverse_lazy('dashboard:sign_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        if order.status == OrderStatus.COMPLETED:
            try:
                delivery_assignment = DeliveryAssignment.objects.get(order=order)
                context['delivery_staff'] = delivery_assignment.delivery_staff
                context['delivery_assigned_at'] = delivery_assignment.assigned_at
                context['delivery_completed_at'] = delivery_assignment.completed_at
            except DeliveryAssignment.DoesNotExist:
                context['delivery_staff'] = None
        return context


class ProductListView(SuperuserRequiredMixin, ListView):
    model = Product
    template_name = 'dashboard/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.all()


class ProductCreateView(SuperuserRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/add/add_new_product.html'
    success_url = reverse_lazy('dashboard:product_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['laptopspec_formset'] = LaptopSpecFormSet(self.request.POST)
        else:
            data['laptopspec_formset'] = LaptopSpecFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        laptopspec_formset = context['laptopspec_formset']
        if form.is_valid() and laptopspec_formset.is_valid():
            product_instance = form.save()
            laptopspec_formset.instance = product_instance
            laptopspec_formset.save()

            # Handle multiple file uploads
            images = self.request.FILES.getlist('images[]')
            for image in images:
                ProductImage.objects.create(product=product_instance, image=image)

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ProductUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/edit/edit_product.html'
    success_url = reverse_lazy('dashboard:product_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['laptopspec_formset'] = LaptopSpecFormSet(self.request.POST, instance=self.object)
        else:
            data['laptopspec_formset'] = LaptopSpecFormSet(instance=self.object)
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        laptopspec_formset = context['laptopspec_formset']
        if laptopspec_formset.is_valid():
            response = super().form_valid(form)
            laptopspec_formset.instance = self.object
            laptopspec_formset.save()
            return response
        else:
            return self.form_invalid(form)


class ProductImageDeleteView(SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        image_id = kwargs.get('pk')
        image = get_object_or_404(ProductImage, id=image_id)
        
        try:
            image.image.delete()  # Delete the image file
            image.delete()  # Delete the database record
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        


class ProductDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('dashboard:product_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)

class GenericModelFormView(SuperuserRequiredMixin, CreateView, UpdateView):
    template_name = 'dashboard/add/generic_form.html'
    
    MODEL_FORM_MAP = {
        'category': (Category, CategoryForm),
        'brand': (Brand, BrandForm),
        'color': (Color, ColorForm),
        'cpubrand': (CpuBrand, CpuBrandForm),
        'gpubrand': (GpuBrand, GpuBrandForm),
        'cpuspec': (CpuSpec, CpuSpecForm),
        'gpuspec': (GpuSpec, GpuSpecForm),
        'memorybrand': (MemoryBrand, MemoryBrandForm),
        'memoryspec': (MemorySpec, MemorySpecForm),
        'storagebrand': (StorageBrand, StorageBrandForm),
        'storagespec': (StorageSpec, StorageSpecForm),
        'displayspec': (DisplaySpec, DisplaySpecForm),
        'portspec': (PortSpec, PortSpecForm),
        'wirelessconnectivity': (WirelessConnectivity, WirelessConnectivityForm),
        'webcamspec': (WebcamSpec, WebcamSpecForm),
        'batteryspec': (BatterySpec, BatterySpecForm),
        'operatingsystem': (OperatingSystem, OperatingSystemForm),
    }

    def dispatch(self, request, *args, **kwargs):
        self.model_name = kwargs.get('model_name')
        self.model, self.form_class = self.MODEL_FORM_MAP.get(self.model_name.lower(), (None, None))
        
        if not self.model or not self.form_class:
            raise Http404("Model not found")
        
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return get_object_or_404(self.model, pk=self.kwargs['pk'])
        return None

    def get_success_url(self):
        return reverse_lazy('dashboard:display_tables')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model_name.capitalize()
        return context

class DisplayTablesView(TemplateView):
    template_name = 'dashboard/table/tables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get instances of all models except LaptopSpec and Product
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['colors'] = Color.objects.all()
        context['cpu_brands'] = CpuBrand.objects.all()
        context['gpu_brands'] = GpuBrand.objects.all()
        context['cpu_specs'] = CpuSpec.objects.all()
        context['gpu_specs'] = GpuSpec.objects.all()
        context['memory_brands'] = MemoryBrand.objects.all()
        context['memory_specs'] = MemorySpec.objects.all()
        context['storage_brands'] = StorageBrand.objects.all()
        context['storage_specs'] = StorageSpec.objects.all()
        context['display_specs'] = DisplaySpec.objects.all()
        context['port_specs'] = PortSpec.objects.all()
        context['wireless_connectivities'] = WirelessConnectivity.objects.all()
        context['webcam_specs'] = WebcamSpec.objects.all()
        context['battery_specs'] = BatterySpec.objects.all()
        context['operating_systems'] = OperatingSystem.objects.all()
        return context


class GenericDeleteView(SuperuserRequiredMixin, View):
    MODEL_MAP = {
        'category': Category,
        'brand': Brand,
        'color': Color,
        'cpubrand': CpuBrand,
        'gpubrand': GpuBrand,
        'cpuspec': CpuSpec,
        'gpuspec': GpuSpec,
        'memorybrand': MemoryBrand,
        'memoryspec': MemorySpec,
        'storagebrand': StorageBrand,
        'storagespec': StorageSpec,
        'displayspec': DisplaySpec,
        'portspec': PortSpec,
        'wirelessconnectivity': WirelessConnectivity,
        'webcamspec': WebcamSpec,
        'batteryspec': BatterySpec,
        'operatingsystem': OperatingSystem,
    }

    def post(self, request, *args, **kwargs):
        model_name = kwargs.get('model_name')
        pk = kwargs.get('pk')
        
        model = self.MODEL_MAP.get(model_name.lower())
        if not model:
            return JsonResponse({'success': False, 'message': 'Model not found'}, status=404)
        
        try:
            instance = get_object_or_404(model, pk=pk)
            instance.delete()
            return JsonResponse({'success': True, 'message': f'{model_name.capitalize()} deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    

class EditModelView(SuperuserRequiredMixin, UpdateView):
    template_name = 'dashboard/edit/edit_model.html'
    success_url = reverse_lazy('dashboard:display_tables')

    MODEL_FORM_MAP = {
        'category': (Category, CategoryForm),
        'brand': (Brand, BrandForm),
        'color': (Color, ColorForm),
        'cpu_brand': (CpuBrand, CpuBrandForm),
        'gpu_brand': (GpuBrand, GpuBrandForm),
        'cpu_spec': (CpuSpec, CpuSpecForm),
        'gpu_spec': (GpuSpec, GpuSpecForm),
        'memory_brand': (MemoryBrand, MemoryBrandForm),
        'memory_spec': (MemorySpec, MemorySpecForm),
        'storage_brand': (StorageBrand, StorageBrandForm),
        'storage_spec': (StorageSpec, StorageSpecForm),
        'display_spec': (DisplaySpec, DisplaySpecForm),
        'port_spec': (PortSpec, PortSpecForm),
        'wireless_connectivity': (WirelessConnectivity, WirelessConnectivityForm),
        'webcam_spec': (WebcamSpec, WebcamSpecForm),
        'battery_spec': (BatterySpec, BatterySpecForm),
        'operating_system': (OperatingSystem, OperatingSystemForm),
    }

    def dispatch(self, request, *args, **kwargs):
        model_name = kwargs.get('model')
        self.model, self.form_class = self.MODEL_FORM_MAP.get(model_name, (None, None))
        
        if not self.model or not self.form_class:
            raise Http404("Model not found")
        
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs.get('model').replace('_', ' ').title()
        return context

class AssignOrderView(SuperuserRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'dashboard/delivery/assign_order.html'
    form_class = AssignOrderForm
    success_url = reverse_lazy('dashboard:assign_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments'] = DeliveryAssignment.objects.filter(
            completed_at__isnull=True
        ).select_related(
            'order', 'delivery_staff__user'
        ).prefetch_related(
            Prefetch('order', queryset=OrderHistory.objects.select_related('user'))
        ).order_by('-assigned_at')
        return context

    def test_func(self):
        return self.request.user.is_superuser

    @method_decorator(transaction.atomic)
    def form_valid(self, form):
        orders = form.cleaned_data['orders']
        delivery_staff = form.cleaned_data['delivery_staff']

        assigned_orders = []
        for order in orders:
            # Check if the order is already assigned
            if hasattr(order, 'delivery_assignment'):
                messages.warning(self.request, f"Order #{order.id} is already assigned and was skipped.")
                continue

            # Create the delivery assignment
            DeliveryAssignment.objects.create(order=order, delivery_staff=delivery_staff)
            assigned_orders.append(order.id)

        # Update delivery staff availability if any orders were assigned
        if assigned_orders:
            delivery_staff.is_available = False
            delivery_staff.save()

            messages.success(self.request, f"Orders #{', '.join(map(str, assigned_orders))} have been assigned to {delivery_staff.user.username}.")
        else:
            messages.warning(self.request, "No orders were assigned. They may already be assigned or an error occurred.")

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error in assigning the orders. Please try again.")
        return super().form_invalid(form)
    
    
    
class DeliveryStaffCreateView(SuperuserRequiredMixin, LoginRequiredMixin, CreateView):
    model = DeliveryStaff
    form_class = DeliveryStaffCreationForm
    template_name = 'delivery/create_delivery_staff.html'
    success_url = reverse_lazy('dashboard:delivery_staff_list')  # Redirect to a page listing all delivery staff members

    def form_valid(self, form):
        # Perform any additional actions if needed
        return super().form_valid(form)

class UserListView(SuperuserRequiredMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/user/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        # Exclude superusers and delivery staff from the customers' table
        return User.objects.filter(is_superuser=False, deliverystaff__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff'] = DeliveryStaff.objects.select_related('user').all()
        context['superusers'] = User.objects.filter(is_superuser=True)
        return context

class UserUpdateView(SuperuserRequiredMixin, LoginRequiredMixin,  UpdateView):
    model = User
    form_class = UserForm
    template_name = 'dashboard/user/user_form.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse_lazy('dashboard:user_list')

class DeliveryStaffUpdateView(SuperuserRequiredMixin, LoginRequiredMixin, UpdateView):
    model = DeliveryStaff
    form_class = DeliveryStaffUserForm
    template_name = 'dashboard/user/staff_form.html'
    context_object_name = 'staff'

    def get_object(self, queryset=None):
        user_id = self.kwargs['pk']
        user = get_object_or_404(User, pk=user_id)
        staff, created = DeliveryStaff.objects.get_or_create(user=user)
        return staff

    def get_success_url(self):
        return reverse_lazy('dashboard:user_list')

class AddSuperuserView(SuperuserRequiredMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'dashboard/user/add_user.html'  # Ensure this matches your actual template path
    success_url = reverse_lazy('dashboard:user_list')  # Replace with your success URL

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.is_superuser = form.cleaned_data['is_superuser']
        user.is_staff = form.cleaned_data['is_staff']
        user.save()
        return super().form_valid(form)