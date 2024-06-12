from django.contrib import admin
from .models import *

class LaptopSpecInLine(admin.StackedInline):
    model = LaptopSpec
    fields = ('cpu', 'memory', 'storage', 'gpu', 'display', 'port', 'wireless_connectivity', 'webcam', 'battery', 'weight', 'operating_system')
    can_delete = False

# class HeadphoneSpecInline(admin.StackedInline):
#     model = HeadphoneSpec
#     fields = ('driver_size', 'frequency_response', 'impedance', 'noise_cancellation', 'connector_type', 'weight', 'battery_life', 'additional_features')
#     can_delete = False

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of additional image slots to show by default

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        LaptopSpecInLine,
        # Add other inlines here if needed
    ]

    fieldsets = (
        (None, {
            'fields': ('name', 'model', 'brand', 'description', 'price', 'category', 'color', 'year', 'warranty_months', 'warranty_years')
        }),
    )

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(LaptopSpec)
admin.site.register(Stock)
admin.site.register(Color)
admin.site.register(CpuBrand)
admin.site.register(GpuBrand)
admin.site.register(CpuSpec)
admin.site.register(GpuSpec)
admin.site.register(MemoryBrand)
admin.site.register(MemorySpec)
admin.site.register(StorageBrand)
admin.site.register(StorageSpec)
admin.site.register(DisplaySpec)
admin.site.register(PortSpec)
admin.site.register(WirelessConnectivity)
admin.site.register(WebcamSpec)
admin.site.register(BatterySpec)
admin.site.register(OperatingSystem)




