from venv import logger
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
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Delivery by: {self.user.username}"

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
        if not self.completed_at:
            try:
                self.completed_at = timezone.now()
                self.save()
                
                self.order.status = OrderStatus.COMPLETED
                self.order.save()
                
                # Set the delivery staff as available
                self.delivery_staff.is_available = True
                self.delivery_staff.save()
                
                DeliveryAssignmentHistory.objects.create(
                    order=self.order,
                    delivery_staff=self.delivery_staff,
                    assigned_at=self.assigned_at,
                    completed_at=self.completed_at
                )
                logger.info(f"Delivery Assignment {self.id} marked as completed, history entry created, and delivery staff set as available.")
            except Exception as e:
                logger.error(f"Error marking delivery {self.id} as completed: {str(e)}")
                raise
        
        
class DeliveryAssignmentHistory(models.Model):
    order = models.ForeignKey(OrderHistory, on_delete=models.CASCADE, related_name='delivery_assignment_history')
    delivery_staff = models.ForeignKey(DeliveryStaff, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField()
    completed_at = models.DateTimeField()

    def __str__(self):
        return f"Delivery History: Order #{self.order.id} - {self.delivery_staff.user.username}"
    
    def get_queryset(self, request):
        # Use the default manager instead of pending_orders
        return super().get_queryset(request).select_related('order', 'delivery_staff__user')