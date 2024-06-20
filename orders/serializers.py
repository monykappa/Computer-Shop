from rest_framework import serializers
from .models import Order, CartItem, OrderHistory, OrderHistoryItem

# serializers.py


class OrderHistoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistoryItem
        fields = '__all__'

class OrderHistorySerializer(serializers.ModelSerializer):
    order_history_items = OrderHistoryItemSerializer(many=True, source='orderhistoryitem_set')

    class Meta:
        model = OrderHistory
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, source='cartitem_set')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cartitem_set')
        order = Order.objects.create(**validated_data)
        for cart_item_data in cart_items_data:
            CartItem.objects.create(order=order, **cart_item_data)
        return order
