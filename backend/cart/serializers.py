# serializers.py in the cart app
from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer  # Assuming you have a ProductSerializer
from django.contrib.auth import get_user_model
from products.models import Product

# CartItem Serializer
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # To include product details in the cart item
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'subtotal']

# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # All items in the cart
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'total_items', 'items']


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)

    def validate_product_id(self, value):
        """
        Validate that the product exists.
        """
        try:
            product = Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")
        return value

    def validate_quantity(self, value):
        """
        Ensure that the quantity is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        """
        Validate that the product exists in the cart.
        """
        try:
            product = Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")
        return value

class CheckoutSerializer(serializers.Serializer):
    def validate(self, data):
        """
        You can add custom validation logic here, e.g., check if the cart is empty.
        """
        cart = Cart.objects.get(user=self.context['request'].user, status='active')
        if not cart.items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        return data
