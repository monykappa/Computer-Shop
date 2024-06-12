from django.contrib import admin
from orders.models import *
from products.models import *
from django.utils.safestring import mark_safe


class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'ordered_date',
        'total_price',
        'status',
        # Add the 'qr_code' field to the change list view
        'qr_code_thumbnail',
    )
    list_display_links = (
        'id',
        'user',
    )
    # Define a method to display a thumbnail of the QR code image
    def qr_code_thumbnail(self, obj):
        if obj.qr_code:
            return mark_safe(f'<img src="{obj.qr_code.url}" width="100" height="100" />')
        else:
            return '(No QR code)'

    qr_code_thumbnail.short_description = 'QR code'

admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(OrderHistoryItem)