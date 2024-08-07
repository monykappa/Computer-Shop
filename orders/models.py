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
from userprofile.models import *
from django.utils import timezone

# Create your models here.


        
class OrderStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    COMPLETED = 'Completed', 'Completed'
    CANCELLED = 'Cancelled', 'Cancelled'


class OrderAddress(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50, choices=CAMBODIAN_PROVINCES)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address1}, {self.city}, {self.province}"

    class Meta:
        verbose_name_plural = "Order Addresses"
        
        
        
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    order_address = models.ForeignKey(OrderAddress, on_delete=models.SET_NULL, null=True, related_name='orders')

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
    order_address = models.ForeignKey(OrderAddress, on_delete=models.SET_NULL, null=True)
    ordered_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)

    @property
    def address(self):
        return self.order_address
    
    
    def address(self):
        # Get the most recent address for the user
        address = Address.objects.filter(user=self.user).last()
        if address:
            return f"{address.address1}, {address.city}, {address.province}"
        return 'No address found'
    
    def __str__(self):
        if self.order_address:
            address_str = f"{self.order_address.address1}, {self.order_address.city}, {self.order_address.province}, {self.order_address.phone}"
        else:
            address_str = 'No address found'
        return f"Order ID #{self.id} - Date: {self.ordered_date.strftime('%Y-%m-%d %H:%M')} - Address: {address_str} - Total: ${self.total_price:.2f}"

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
    
    def has_been_rated(self):
        return ProductRating.objects.filter(order_history_item=self).exists()
    

class ProductRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_history_item = models.ForeignKey(OrderHistoryItem, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product', 'order_history_item')

    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star rating for {self.product.name}"