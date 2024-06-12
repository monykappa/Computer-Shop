from fileinput import filename
from typing_extensions import Buffer
from django.db import models
from products.models import *
from io import BytesIO
from django.core.files import File
from PIL import Image
import qrcode
from django.urls import reverse
from decimal import Decimal

# Create your models here.

class OrderStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    COMPLETED = 'Completed', 'Completed'
    CANCELLED = 'Cancelled', 'Cancelled'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def calculate_total_price(self):
        # Calculate total price based on cart items
        total = Decimal(0)
        for item in self.cartitem_set.all():
            total += item.subtotal
        self.total_price = total
        self.save()
        
    def __str__(self):
        return f"Order #{self.id} - Total: ${self.total_price:.2f}"

class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"CartItem #{self.id} - {self.product} - Quantity: {self.quantity} - Subtotal: ${self.subtotal:.2f}"

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)
        order_items = self.order.cartitem_set.all()
        self.order.total_price = sum(item.subtotal for item in order_items)
        self.order.save()

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)

    def __str__(self):
        return f"Order History #{self.id} - {self.ordered_date} - Total: ${self.total_price:.2f}"

    def update_status(self, new_status):
        if new_status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            self.status = new_status
            self.save()
            
    def generate_qr_code(self, request):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Construct the full URL with the request object
        host = request.get_host()
        qr_data = f'http://{host}{reverse("orders:order_history_image", args=[self.id])}'
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        buffer.seek(0)  # Ensure the pointer is at the start of the buffer

        # Save the QR code image to the qr_code field
        file_name = f'order_{self.id}_qr.png'
        self.qr_code.save(file_name, File(buffer), save=True)


class OrderHistoryItem(models.Model):
    order_history = models.ForeignKey(OrderHistory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def product_details(self):
        return f"{self.product.brand_name} - {self.product.description}"