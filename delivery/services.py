from django.contrib.auth.models import User
from .models import DeliveryStaff, DeliveryAssignment

def create_delivery_staff(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    user.is_staff = True
    user.save()
    delivery_staff = DeliveryStaff.objects.create(user=user)
    return delivery_staff

def assign_order_to_delivery_staff(order, delivery_staff):
    return DeliveryAssignment.objects.create(order=order, delivery_staff=delivery_staff)