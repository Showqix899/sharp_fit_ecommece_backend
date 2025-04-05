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
        queryset=Size.objects.all(),
        many=True,
        write_only=True
    )
    color_ids = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(),
        many=True,
        write_only=True
    )

    # Category field
    category = serializers.ChoiceField(
        choices=Product.CATEGORY_CHOICES
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock',
            'category', 'sizes', 'colors', 'size_ids', 'color_ids',
            'image', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        size_ids = validated_data.pop('size_ids', [])
        color_ids = validated_data.pop('color_ids', [])
        product = Product.objects.create(**validated_data)
        product.sizes.set(size_ids)
        product.colors.set(color_ids)
        return product

    def update(self, instance, validated_data):
        size_ids = validated_data.pop('size_ids', None)
        color_ids = validated_data.pop('color_ids', None)

        if size_ids is not None:
            instance.sizes.set(size_ids)
        if color_ids is not None:
            instance.colors.set(color_ids)

        return super().update(instance, validated_data)
