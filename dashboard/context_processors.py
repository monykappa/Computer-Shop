from django.template.context_processors import request
from orders.models import *

def pending_order_count(request):
    return {'pending_order_count': OrderHistory.objects.filter(status='Pending').count()}

def order_history_processor(request):
    latest_orders = OrderHistory.objects.all().order_by('-ordered_date')[:20]
    pending_orders_exist = OrderHistory.objects.filter(status='Pending').exists()
    return {
        'order_history': latest_orders,
        'pending_orders_exist': pending_orders_exist
    }