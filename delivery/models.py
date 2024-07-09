from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from orders.models import *

class PendingOrderHistoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            order__status=OrderStatus.PENDING,
            order__delivery_assignment__isnull=True
        )

class DeliveryStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Delivery Staff: {self.user.username}"

class DeliveryAssignment(models.Model):
    order = models.OneToOneField(OrderHistory, on_delete=models.CASCADE, related_name='delivery_assignment')
    delivery_staff = models.ForeignKey(DeliveryStaff, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()  # The default manager
    pending_orders = PendingOrderHistoryManager()  # Custom manager for pending orders

    def __str__(self):
        return f"Delivery Assignment: Order History #{self.order.id} - {self.delivery_staff.user.username}"

    def mark_completed(self):
        self.completed_at = timezone.now()
        self.save()
        # Update the order status in the OrderHistory model
        self.order.update_status(OrderStatus.COMPLETED)