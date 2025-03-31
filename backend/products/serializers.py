from rest_framework import serializers
from .models import Product, Size, Color

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

from rest_framework import serializers
from .models import Product, Size, Color

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(read_only=True)  # Only one size
    colors = ColorSerializer(read_only=True)  # Only one color
    size_id = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(), write_only=True
    )
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'sizes', 'colors', 'size_id', 'color_id', 'image']

    def create(self, validated_data):
        size = validated_data.pop('size_id')  # Extract size
        color = validated_data.pop('color_id')  # Extract color
        product = Product.objects.create(sizes=size, colors=color, **validated_data)
        return product

    def update(self, instance, validated_data):
        instance.sizes = validated_data.get('size_id', instance.sizes)
        instance.colors = validated_data.get('color_id', instance.colors)
        return super().update(instance, validated_data)
