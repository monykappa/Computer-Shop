from django import forms
from products.models import *
from django.forms.widgets import FileInput
from django.forms import inlineformset_factory
from delivery.models import *

class UserForm(forms.ModelForm):
    is_superuser = forms.BooleanField(label='Superuser', required=False)
    is_staff = forms.BooleanField(label='Staff', required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input ml-5'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input ml-5'}),
        }

# forms.py (continued)
class UserUpdateForm(forms.ModelForm):
    is_superuser = forms.BooleanField(label='Superuser', required=False)
    is_staff = forms.BooleanField(label='Staff', required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input ml-5'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input ml-5'}),
        }


class BaseUserForm(forms.ModelForm):
    is_superuser = forms.BooleanField(label='Superuser', required=False)
    is_staff = forms.BooleanField(label='Staff', required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input ml-5'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input ml-5'}),
        }

class UserAddForm(BaseUserForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta(BaseUserForm.Meta):
        fields = BaseUserForm.Meta.fields + ['password']


class DeliveryStaffForm(forms.ModelForm):
    class Meta:
        model = DeliveryStaff
        fields = ['phone_number', 'is_available']
        
        
class MultipleFileInput(FileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs.update({'multiple': 'multiple'})
        self.attrs = attrs

class LaptopSpecForm(forms.ModelForm):
    class Meta:
        model = LaptopSpec
        fields = [
            'cpu', 'gpu', 'memory', 'storage', 'display', 'webcam',
            'battery', 'weight', 'operating_system', 'port', 'wireless_connectivity'
        ]
        widgets = {
            'cpu': forms.Select(attrs={'class': 'form-control'}),
            'gpu': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'memory': forms.Select(attrs={'class': 'form-control'}),
            'storage': forms.Select(attrs={'class': 'form-control'}),
            'display': forms.Select(attrs={'class': 'form-control'}),
            'webcam': forms.Select(attrs={'class': 'form-control'}),
            'battery': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'operating_system': forms.Select(attrs={'class': 'form-control'}),
            'port': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'wireless_connectivity': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    images = forms.FileField(widget=MultipleFileInput(), required=False)

    class Meta:
        model = Product
        exclude = ['slug', 'cpu', 'gpu', 'memory', 'storage', 'display', 'port', 'wireless_connectivity', 'webcam', 'battery', 'operating_system']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        instance = super(ProductForm, self).save(commit=False)
        if commit:
            instance.save()
            images = self.files.getlist('images')
            for image in images:
                ProductImage.objects.create(product=instance, image=image)
        return instance

LaptopSpecFormSet = inlineformset_factory(
    Product, LaptopSpec, form=LaptopSpecForm, extra=1, can_delete=False
)

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BrandForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo']

class ColorForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Color
        fields = ['name']

class CpuBrandForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CpuBrand
        fields = ['name']

class GpuBrandForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = GpuBrand
        fields = ['name']

class CpuSpecForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CpuSpec
        fields = ['model', 'cpu_brand', 'cores', 'threads', 'cpu_detail']

class GpuSpecForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = GpuSpec
        fields = ['model', 'gpu_brand', 'vram', 'vram_type', 'gpu_detail']

class MemoryBrandForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = MemoryBrand
        fields = ['name']

class MemorySpecForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = MemorySpec
        fields = ['capacity', 'type', 'speed', 'memory_brand']

class StorageBrandForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = StorageBrand
        fields = ['name']

class StorageSpecForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = StorageSpec
        fields = [
            'storage_brand', 'type', 'capacity', 'capacity_type', 
            'interface', 'read_speed', 'write_speed', 'form_factor'
        ]

class DisplaySpecForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = DisplaySpec
        fields = ['display', 'display_detail']

class PortSpecForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PortSpec
        fields = ['port']

class WirelessConnectivityForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = WirelessConnectivity
        fields = ['wireless_connectivity']

class WebcamSpecForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = WebcamSpec
        fields = ['webcam', 'webcam_detail']

class BatterySpecForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = BatterySpec
        fields = ['battery', 'battery_detail']

class OperatingSystemForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = OperatingSystem
        fields = ['operating_system', 'operating_system_detail']