from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from .models import Product, Size, Color
from .serializers import ProductSerializer, SizeSerializer, ColorSerializer

from .models import Product, Size, Color
from .serializers import ProductSerializer, SizeSerializer, ColorSerializer
from rest_framework.parsers import MultiPartParser, FormParser



#size view
class SizeListCreateView(generics.ListCreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


#color view
class ColorListCreateView(generics.ListCreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


#listing and creating Product view
class ProductListCreateView(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        cache_key= f'product_{user.id}'
        cached_products = cache.get(cache_key)

        if cached_products:
            return Response(cached_products, status=status.HTTP_200_OK)
        else:
            products=Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            cache.set(cache_key, serializer.data, timeout=60*5) # seting cache for 5 minutes
  
            return Response(serializer.data, status=status.HTTP_200_OK)


# Product Create View (POST request only)
class ProductCreateView(generics.CreateAPIView):
    parser_classes=(MultiPartParser,FormParser)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # Create the product object
        product = serializer.save()
        # Clear the cache for the user's product list after product creation
        user = self.request.user
        cache.delete(f'product_{user.id}')  # Clear cache when a new product is added
        return product      


# Product Retrieve View (GET request for details)
class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer





# Product Update View (PUT request for update)
class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        # Update the product object
        product = serializer.save()
        # Clear the cache for the user's product list
        user = self.request.user
        cache.delete(f'product_list_{user.id}')  # Clear cache when a product is updated
        # Optionally, you can cache the updated product
        cache.set(f'product_{product.id}', ProductSerializer(product).data, timeout=60*5)
        return product

# Product Destroy View (DELETE request to remove a product)
class ProductDestroyView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        # Delete the product
        instance.delete()
        # Clear the cache for the user's product list
        user = self.request.user
        cache.delete(f'product_list_{user.id}')  # Clear cache when a product is deleted
        return instance
