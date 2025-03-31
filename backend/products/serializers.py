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
    sizes = SizeSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    size_ids = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(), write_only=True, many=True
    )
    color_ids = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), write_only=True, many=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'sizes', 'colors', 'size_ids', 'color_ids', 'image']

    def create(self, validated_data):
        #get the selected  size ids
        size_ids = validated_data.pop('size_ids', [])
        #get the selected colors ids
        color_ids = validated_data.pop('color_ids', [])
        product = Product.objects.create(**validated_data)
        product.sizes.set(size_ids) #seting the size ids
        product.colors.set(color_ids) # seting the color ids
        return product

    def update(self, instance, validated_data):
        size_ids = validated_data.pop('size_ids', [])
        color_ids = validated_data.pop('color_ids', [])
        instance.sizes.set(size_ids)
        instance.colors.set(color_ids)
        return super().update(instance, validated_data)
