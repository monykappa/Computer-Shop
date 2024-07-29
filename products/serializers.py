from rest_framework import serializers
from .models import (
    Category, Brand, Color, Product, ProductImage, CpuBrand, GpuBrand, 
    CpuSpec, GpuSpec, MemoryBrand, MemorySpec, StorageBrand, StorageSpec, 
    DisplaySpec, PortSpec, WirelessConnectivity, WebcamSpec, BatterySpec, 
    OperatingSystem, LaptopSpec, Stock, RefreshRate, ResolutionSpec
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo', 'slug']

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'slug']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    color = ColorSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'model', 'brand', 'description', 'price', 'category',
            'color', 'year', 'warranty_months', 'warranty_years', 'slug', 'images'
        ]

class CpuBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CpuBrand
        fields = ['id', 'name', 'slug']

class GpuBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpuBrand
        fields = ['id', 'name', 'slug']

class CpuSpecSerializer(serializers.ModelSerializer):
    cpu_brand = CpuBrandSerializer()

    class Meta:
        model = CpuSpec
        fields = ['id', 'model', 'cpu_brand', 'cores', 'threads', 'cpu_detail', 'slug']

class GpuSpecSerializer(serializers.ModelSerializer):
    gpu_brand = GpuBrandSerializer()

    class Meta:
        model = GpuSpec
        fields = ['id', 'model', 'gpu_brand', 'vram', 'vram_type', 'gpu_detail', 'slug']

class MemoryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryBrand
        fields = ['id', 'name', 'slug']

class MemorySpecSerializer(serializers.ModelSerializer):
    memory_brand = MemoryBrandSerializer()

    class Meta:
        model = MemorySpec
        fields = ['id', 'capacity', 'type', 'speed', 'memory_brand', 'slug']

class StorageBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageBrand
        fields = ['id', 'name', 'slug']

class StorageSpecSerializer(serializers.ModelSerializer):
    storage_brand = StorageBrandSerializer()

    class Meta:
        model = StorageSpec
        fields = [
            'id', 'storage_brand', 'type', 'capacity', 'capacity_type', 
            'interface', 'read_speed', 'write_speed', 'form_factor', 'slug'
        ]

class DisplaySpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplaySpec
        fields = ['id', 'display', 'display_detail', 'slug']

class ResolutionSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResolutionSpec
        fields = ['id', 'resolution']

class RefreshRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshRate
        fields = ['id', 'rate']

class PortSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortSpec
        fields = ['id', 'port', 'slug']

class WirelessConnectivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WirelessConnectivity
        fields = ['id', 'wireless_connectivity', 'slug']

class WebcamSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebcamSpec
        fields = ['id', 'webcam', 'webcam_detail', 'slug']

class BatterySpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatterySpec
        fields = ['id', 'battery', 'battery_detail', 'slug']

class OperatingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingSystem
        fields = ['id', 'operating_system', 'operating_system_detail', 'slug']

class LaptopSpecSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cpu = CpuSpecSerializer()
    memory = MemorySpecSerializer()
    storage = StorageSpecSerializer()
    gpu = GpuSpecSerializer(many=True)
    display = DisplaySpecSerializer()
    resolution = ResolutionSpecSerializer()
    refresh_rate = RefreshRateSerializer()
    port = PortSpecSerializer(many=True)
    wireless_connectivity = WirelessConnectivitySerializer(many=True)
    webcam = WebcamSpecSerializer()
    battery = BatterySpecSerializer()
    operating_system = OperatingSystemSerializer()

    class Meta:
        model = LaptopSpec
        fields = [
            'id', 'product', 'cpu', 'memory', 'storage', 'gpu', 'display', 'resolution', 'refresh_rate', 'port',
            'wireless_connectivity', 'webcam', 'battery', 'weight', 'operating_system', 'slug'
        ]

class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Stock
        fields = ['id', 'product', 'quantity', 'price_per_unit', 'total_price', 'price_per_unit_with_dollar', 'total_price_with_dollar']
