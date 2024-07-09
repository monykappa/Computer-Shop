from django.contrib import admin
from django.utils import timezone
from .models import DeliveryStaff, DeliveryAssignment
from orders.models import OrderHistory, OrderStatus

@admin.register(DeliveryStaff)
class DeliveryStaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('user__username', 'user__email')

@admin.register(DeliveryAssignment)
class DeliveryAssignmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_staff', 'assigned_at_display', 'completed_at_display', 'order_status')
    list_filter = ('assigned_at', 'completed_at')
    search_fields = ('order__id', 'delivery_staff__user__username')

    def get_queryset(self, request):
        return DeliveryAssignment.pending_orders.select_related('order', 'delivery_staff__user')

    def assigned_at_display(self, obj):
        return timezone.localtime(obj.assigned_at) if obj.assigned_at else None
    assigned_at_display.short_description = 'Assigned At'

    def completed_at_display(self, obj):
        return timezone.localtime(obj.completed_at) if obj.completed_at else None
    completed_at_display.short_description = 'Completed At'

    def order_status(self, obj):
        return obj.order.status
    order_status.short_description = 'Order Status'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "order":
            kwargs["queryset"] = OrderHistory.objects.filter(status=OrderStatus.PENDING)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)