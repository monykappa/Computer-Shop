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
from bokeh.plotting import figure
from bokeh.embed import components
from plotly.offline import plot
import plotly.graph_objs as go
from userprofile.models import *
from .forms import *
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponseForbidden







# Create your views here.

class DashboardView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    login_url = reverse_lazy('dashboard:sign_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = Product.objects.count()
        context['total_orders'] = OrderHistory.objects.count()
        context['total_users'] = User.objects.count()

        # Retrieve the newest product
        newest_product = Product.objects.latest('id')
        context['newest_product_name'] = newest_product.name
        return context

class DashboardSignInView(LoginView):
    template_name = 'dashboard/sign_in.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('dashboard:dashboard')

class DashboardLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('dashboard:sign_in')


class OrderHistoryView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = OrderHistory
    template_name = 'dashboard/orders.html'
    context_object_name = 'order_histories'
    paginate_by = 10  

    def get_queryset(self):
        # Filter the order history by the logged-in user and status
        status = self.request.GET.get('status', OrderStatus.PENDING)
        return OrderHistory.objects.filter(user=self.request.user, status=status).order_by('-ordered_date')

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
            messages.success(request, f'Order {order_history.id} has been updated to {new_status}')
        else:
            messages.error(request, 'Invalid status')
        return redirect('dashboard:order')


class OrderDetailView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    model = OrderHistory
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'order'
    login_url = reverse_lazy('dashboard:sign_in')


class ProductListView(ListView, SuperuserRequiredMixin):
    model = Product
    template_name = 'dashboard/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.all()


class ProductCreateView(CreateView, SuperuserRequiredMixin):
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
        if laptopspec_formset.is_valid():
            product_instance = form.save()
            laptopspec_formset.instance = product_instance
            laptopspec_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ProductUpdateView(UpdateView, SuperuserRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = 'dashboard/edit/edit_product.html'
    success_url = reverse_lazy('dashboard:product_list')

    def get_context_data(self, **kwargs):
        data = super(ProductUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['laptopspec_formset'] = LaptopSpecFormSet(self.request.POST, instance=self.object)
        else:
            data['laptopspec_formset'] = LaptopSpecFormSet(instance=self.object)
        data['product'] = self.object  # Ensure the product instance is added to context
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



class ProductDeleteView(DeleteView, SuperuserRequiredMixin):
    model = Product
    success_url = reverse_lazy('dashboard:product_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)

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


class EditModelView(UpdateView):
    template_name = 'dashboard/edit/edit_model.html'
    model = None
    fields = '__all__'
    success_url = reverse_lazy('dashboard:display_tables')

    def get_object(self, queryset=None):
        model_name = self.kwargs.get('model')
        if model_name == 'category':
            self.model = Category
        elif model_name == 'brand':
            self.model = Brand
        elif model_name == 'color':
            self.model = Color
        elif model_name == 'cpu_brand':
            self.model = CpuBrand
        elif model_name == 'gpu_brand':
            self.model = GpuBrand
        elif model_name == 'cpu_spec':
            self.model = CpuSpec
        elif model_name == 'gpu_spec':
            self.model = GpuSpec
        elif model_name == 'memory_brand':
            self.model = MemoryBrand
        elif model_name == 'memory_spec':
            self.model = MemorySpec
        elif model_name == 'storage_brand':
            self.model = StorageBrand
        elif model_name == 'storage_spec':
            self.model = StorageSpec
        elif model_name == 'display_spec':
            self.model = DisplaySpec
        elif model_name == 'port_spec':
            self.model = PortSpec
        elif model_name == 'wireless_connectivity':
            self.model = WirelessConnectivity
        elif model_name == 'webcam_spec':
            self.model = WebcamSpec
        elif model_name == 'battery_spec':
            self.model = BatterySpec
        elif model_name == 'operating_system':
            self.model = OperatingSystem
        return super().get_object(queryset)

    def get_form_class(self):
        form_class = super().get_form_class()
        if hasattr(self.model, 'slug'):
            fields = form_class.Meta.fields
            fields = [field for field in fields if field != 'slug']
            form_class.Meta.fields = fields
        return form_class
