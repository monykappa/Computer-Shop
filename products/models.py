from django.db import models
from django.core.exceptions import ValidationError
import os
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from .mixins import SlugMixin 

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def product_directory_path(instance, filename):
    unique_id = str(uuid.uuid4())
    directory_path = f'content/{unique_id}/'
    return os.path.join(directory_path, filename)

def product_related_images_directory_path(instance, filename):
    unique_id = str(uuid.uuid4())
    directory_path = f'product_related_images/{unique_id}/'
    return os.path.join(directory_path, filename)

class Category(SlugMixin):
    name = models.CharField(max_length=100)

    @property
    def slug_source(self):
        return self.name

    def __str__(self):
        return self.name

class Brand(SlugMixin):
    name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.FileField(upload_to=product_directory_path, validators=[validate_file_extension], blank=True, null=True)

    @property
    def slug_source(self):
        return self.name

    def __str__(self):
        return self.name

class Color(SlugMixin):
    name = models.CharField(max_length=100)
    @property
    def slug_source(self):
        return f"{self.name}"
    
    def __str__(self):
        return self.name

class Product(SlugMixin):
    name = models.CharField(max_length=200, null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True) 
    year = models.CharField(max_length=4, choices=[(str(year), str(year)) for year in range(2015, 2056)], null=True, blank=True)
    warranty_months = models.IntegerField(null=True, blank=True)
    warranty_years = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def slug_source(self):
        return f"{self.name} {self.model}"

    def __str__(self):
        price_str = f"{self.price:.2f}".rstrip('0').rstrip('.')
        return f"{self.name} - {self.model} -  ${price_str} - {self.year}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to=product_directory_path, validators=[validate_file_extension])

    def __str__(self):
        return f"Image for {self.product.name}"


class CpuBrand(SlugMixin):
    name = models.CharField(max_length=100, null=True, blank=True)
    @property
    def slug_source(self):
        return self.name if self.name else "cpu-brand"

    def __str__(self):
        return f"{self.name}" if self.name else "Unassociated CPU Brand"

class GpuBrand(SlugMixin):
    name = models.CharField(max_length=100, null=True, blank=True)
    @property
    def slug_source(self):
        return self.name if self.name else "gpu-brand"

    def __str__(self):
        return f"{self.name}" if self.name else "Unassociated GPU Brand"
    
class CpuSpec(SlugMixin):
    model = models.CharField(max_length=100, null=True, blank=True)
    cpu_brand = models.ForeignKey(CpuBrand, on_delete=models.CASCADE, null=True, blank=True)
    cores = models.CharField(max_length=100, null=True, blank=True)
    threads = models.CharField(max_length=100, null=True, blank=True)
    cpu_detail = models.CharField(max_length=200, null=True, blank=True)

    @property
    def slug_source(self):
        return self.model if self.model else "cpu-spec"

    def __str__(self):
        return f"{self.cpu_brand} - {self.model} - {self.cores} cores - {self.threads} threads" if self.model else "Unassociated CPU Specifications"


class GpuSpec(SlugMixin):
    model = models.CharField(max_length=100, null=True, blank=True)
    gpu_brand = models.ForeignKey(GpuBrand, on_delete=models.CASCADE, null=True, blank=True)
    vram = models.CharField(max_length=100, null=True, blank=True)
    vram_type = models.CharField(max_length=100, null=True, blank=True)
    gpu_detail = models.CharField(max_length=200, null=True, blank=True)

    @property
    def slug_source(self):
        return self.model if self.model else "gpu-spec"

    def __str__(self):
        return f"{self.gpu_brand} - {self.model} - {self.vram} GB VRAM - {self.vram_type}" if self.model else "Unassociated GPU Specifications"

class MemoryBrand(SlugMixin):
    name = models.CharField(max_length=100, null=True, blank=True)
    
    @property
    def slug_source(self):
        return self.name if self.name else "memory-brand"

    def __str__(self):
        return f"{self.name}" if self.name else "Unassociated Memory Brand"
    
class MemorySpec(SlugMixin):
    capacity = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)
    memory_brand = models.ForeignKey(MemoryBrand, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def slug_source(self):
        return self.capacity if self.capacity else "memory-spec"

    def __str__(self):
        return f"{self.memory_brand.name} - {self.capacity}GB - {self.type}" if self.capacity else "Unassociated Memory Specifications"


class StorageBrand(SlugMixin):
    name = models.CharField(max_length=100, null=True, blank=True)

    @property
    def slug_source(self):
        return self.name if self.name else "storage-spec"

    def __str__(self):
        return f"{self.name}" if self.name else "Unassociated Storage Specifications"
    
class StorageSpec(SlugMixin):
    GB = 'GB'
    TB = 'TB'
    CAPACITY_CHOICES = [
        (GB, 'GB'),
        (TB, 'TB'),
    ]
    storage_brand = models.ForeignKey(StorageBrand, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    capacity_type = models.CharField(max_length=100, choices=CAPACITY_CHOICES, default=GB)  # Default to GB
    interface = models.CharField(max_length=100, null=True, blank=True)
    read_speed = models.IntegerField(null=True, blank=True)
    write_speed = models.IntegerField(null=True, blank=True)
    form_factor = models.CharField(max_length=100, null=True, blank=True)

    @property
    def slug_source(self):
        return self.capacity if self.capacity else "storage-spec"

    def __str__(self):
        return f"{self.capacity} {self.capacity_type}" if self.capacity else "Unassociated Storage Specifications"


class DisplaySpec(SlugMixin):
    display = models.CharField(max_length=100, null=True, blank=True)
    display_detail = models.CharField(max_length=200, null=True, blank=True)

    @property
    def slug_source(self):
        return self.display if self.display else "display-spec"

    def __str__(self):
        return f"{self.display} inches - {self.display_detail} panel" if self.display else "Unassociated Display Specifications"


class ResolutionSpec(SlugMixin):
    RESOLUTION_CHOICES = [
        ('HD', 'HD'),
        ('Full HD', 'Full HD'),
        ('2K', '2K'),
        ('4K', '4K'),
    ]
    resolution = models.CharField(max_length=100, choices=RESOLUTION_CHOICES, null=True, blank=True)
    
    @property
    def slug_source(self):
        return self.resolution if self.resolution else "resolution-spec"

    def __str__(self):
        return f"{self.resolution}"
    
    
class PortSpec(SlugMixin):
    port = models.CharField(max_length=100, null=True, blank=True)

    @property
    def slug_source(self):
        return self.port if self.port else "port-spec"

    def __str__(self):
        return f"{self.port}" if self.port else "Unassociated Port Specifications"

class WirelessConnectivity(SlugMixin):
    wireless_connectivity = models.CharField(max_length=100, null=True, blank=True)


    @property
    def slug_source(self):
        return self.wireless_connectivity if self.wireless_connectivity else "wireless-connectivity-spec"

    def __str__(self):
        return f"{self.wireless_connectivity}" if self.wireless_connectivity else "Unassociated Wireless Connectivity Specifications"

class WebcamSpec(SlugMixin):
    webcam = models.CharField(max_length=100, null=True, blank=True)
    webcam_detail = models.CharField(max_length=200, null=True, blank=True)

    @property
    def slug_source(self):
        return self.webcam if self.webcam else "webcam-spec"

    def __str__(self):
        return f"{self.webcam} - {self.webcam_detail}" if self.webcam else "Unassociated Webcam Specifications"

class BatterySpec(SlugMixin):
    battery = models.IntegerField(null=True, blank=True)
    battery_detail = models.CharField(max_length=200, null=True, blank=True)

    @property
    def slug_source(self):
        return self.battery if self.battery else "battery-spec"

    def __str__(self):
        return f"{self.battery} Kw" if self.battery else "Unassociated Battery Specifications"

class OperatingSystem(SlugMixin):
    operating_system = models.CharField(max_length=100, null=True, blank=True)
    operating_system_detail = models.CharField(max_length=200, null=True, blank=True)

    @property
    def slug_source(self):
        return self.operating_system if self.operating_system else "operating-system-spec"

    def __str__(self):
        return f"{self.operating_system}" if self.operating_system else "Unassociated Operating System Specifications"    

class RefreshRate(models.Model):
    rate = models.CharField(max_length=50, unique=True)  # Store refresh rate, e.g., "60Hz", "144Hz"

    def __str__(self):
        return self.rate
    
class LaptopSpec(SlugMixin):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='laptop_spec')
    cpu = models.ForeignKey(CpuSpec, on_delete=models.CASCADE,  null=True, blank=True)
    memory = models.ForeignKey(MemorySpec, on_delete=models.CASCADE,  null=True, blank=True)
    storage = models.ForeignKey(StorageSpec, on_delete=models.CASCADE, null=True, blank=True)
    gpu = models.ManyToManyField(GpuSpec, blank=True) 
    display = models.ForeignKey(DisplaySpec, on_delete=models.CASCADE, null=True, blank=True)
    resolution = models.ForeignKey(ResolutionSpec, on_delete=models.CASCADE, null=True, blank=True)
    refresh_rate = models.ForeignKey(RefreshRate, on_delete=models.CASCADE, null=True, blank=True)
    port = models.ManyToManyField(PortSpec, blank=True)
    wireless_connectivity = models.ManyToManyField(WirelessConnectivity, blank=True)
    webcam = models.ForeignKey(WebcamSpec, on_delete=models.CASCADE, null=True, blank=True)
    battery = models.ForeignKey(BatterySpec, on_delete=models.CASCADE, max_length=100, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def slug_source(self):
        return self.product if self.product else "battery-spec"
    
    def __str__(self):
        return f"Specifications for {self.product.name} {self.product.model}" if self.product else "Unassociated Laptop Specifications"



class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} - {self.product.model} - {self.quantity} units in stock"

    def price_per_unit(self):
        return self.product.price if self.product else 0

    def total_price(self):
        return self.price_per_unit() * self.quantity

    def price_per_unit_with_dollar(self):
        return f"${self.price_per_unit():.2f}"

    def total_price_with_dollar(self):
        return f"${self.total_price():.2f}"

    def is_available(self):
        return self.quantity > 0