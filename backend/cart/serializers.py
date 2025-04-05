from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product, Size, Color
from products.serializers import ProductSerializer


# CartItem Serializer for viewing cart
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['product', 'size', 'color', 'quantity', 'subtotal']


# Cart Serializer for viewing cart
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'total_items', 'items']

    def get_total_price(self, obj):
        return obj.total_price()

    def get_total_items(self, obj):
        return obj.total_items()


# Serializer for adding product to cart
class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    size = serializers.IntegerField()
    color = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        user = self.context['request'].user
        product_id = data.get('product_id')
        size_id = data.get('size')
        color_id = data.get('color')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_id': 'Invalid product.'})

        try:
            size_obj = Size.objects.get(id=size_id)
        except Size.DoesNotExist:
            raise serializers.ValidationError({'size': 'Invalid size selected.'})

        try:
            color_obj = Color.objects.get(id=color_id)
        except Color.DoesNotExist:
            raise serializers.ValidationError({'color': 'Invalid color selected.'})

        # Ensure the selected size and color are valid for the product
        if not product.sizes.filter(id=size_id).exists():
            raise serializers.ValidationError({'size': 'This size is not available for the selected product.'})
        if not product.colors.filter(id=color_id).exists():
            raise serializers.ValidationError({'color': 'This color is not available for the selected product.'})

        # Check if cart item already exists with same combination
        cart, _ = Cart.objects.get_or_create(user=user, status='active')
        if CartItem.objects.filter(cart=cart, product=product, size=size_obj.name, color=color_obj.name).exists():
            raise serializers.ValidationError("This product with the selected size and color is already in your cart.")

        return data


# Serializer for removing from cart
class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product.")
        return value


# Checkout (you already had this, kept as-is)
class CheckoutSerializer(serializers.Serializer):
    def validate(self, data):
        cart = Cart.objects.get(user=self.context['request'].user, status='active')
        if not cart.items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        return data
