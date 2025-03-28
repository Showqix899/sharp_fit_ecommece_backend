# from rest_framework import serializers
# from .models import Product, Size, Color

# class SizeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Size
#         fields = ['id', 'name']

# class ColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Color
#         fields = ['id', 'name']

# class ProductSerializer(serializers.ModelSerializer):
#     sizes = SizeSerializer(many=True, read_only=True)
#     colors = ColorSerializer(many=True, read_only=True)

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'price', 'image', 'sizes', 'colors']
