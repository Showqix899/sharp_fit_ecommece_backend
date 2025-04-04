# serializers.py in the cart app
from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer  # Assuming you have a ProductSerializer
from django.contrib.auth import get_user_model
from products.models import Product,Size,Color

# CartItem Serializer
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # To include product details in the cart item
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['product','size','color', 'quantity', 'subtotal']

# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # All items in the cart
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'total_items', 'items']




# AddToCart Serializer
class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    size = serializers.IntegerField(required=True)  # Ensure it's an ID, not a CharField
    color = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(default=1)

    def validate(self, data):
        product_id = data.get('product_id')
        size_id = data.get('size')
        color_id = data.get('color')

        # Validate Product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_id': 'Product not found.'})

        # Validate Size
        try:
            size = Size.objects.get(id=size_id)
        except Size.DoesNotExist:
            raise serializers.ValidationError({'size': 'Invalid size selected.'})

        # Validate Color
        try:
            color = Color.objects.get(id=color_id)
        except Color.DoesNotExist:
            raise serializers.ValidationError({'color': 'Invalid color selected.'})

        # Check if this product matches the provided size and color
        if product.sizes != size or product.colors != color:
            raise serializers.ValidationError("Product with the selected size and color not found.")

        return data
        

        
        
# cart remove serializer
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

# Checkout Serializer
class CheckoutSerializer(serializers.Serializer):
    def validate(self, data):
        """
        You can add custom validation logic here, e.g., check if the cart is empty.
        """
        cart = Cart.objects.get(user=self.context['request'].user, status='active')
        if not cart.items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        return data
