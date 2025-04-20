from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'total_price', 'status', 'items', 'created_at', 'updated_at']



class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user=serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'total_price', 'status', 'items', 'created_at', 'updated_at']

    def get_user(self,obj):
        return obj.user.email if obj.user else None
    
