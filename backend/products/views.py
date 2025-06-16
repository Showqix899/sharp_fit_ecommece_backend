from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsAdminUser




from django.core.cache import cache

from .models import Product, Size, Color
from .serializers import ProductSerializer, SizeSerializer, ColorSerializer

from .models import Product, Size, Color
from .serializers import ProductSerializer, SizeSerializer, ColorSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Q


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


# Product Create View (POST request only)   (only for admin)
class ProductCreateView(generics.CreateAPIView):
    parser_classes=(MultiPartParser,FormParser)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser,IsAuthenticated]

    def perform_create(self, serializer):
        # Create the product object
        product = serializer.save()
        price = product.price
        discount = product.discount
        if discount:
            final_price = price - (price * (discount / 100))
            product.price = final_price
            product.save()
        # Clear the cache for the user's product list after product creation
        user = self.request.user
        cache.delete(f'product_{user.id}')  # Clear cache when a new product is added
        return product      


# Product Retrieve View (GET request for details)
class ProductRetrieveView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self,request):

        name = request.query_params.get('name')
        description = request.query_params.get('description')
        category = request.query_params.get('category')
        color = request.query_params.get('color')
        size = request.query_params.get('size')
        
        name = name.lower() if name else None
        description = description.lower() if description else None
        filters = Q()

        if name:
            filters &= Q(name__icontains=name)
        if description:
            filters &= Q(description__icontains=description)
        if category:
            filters &= Q(category__iexact=category)
        if color:
            filters &= Q(colors__name__iexact=color)
        if size:
            filters &= Q(sizes__name__iexact=size)


        product = Product.objects.filter(filters).distinct().first()

        if not product:
            return Response({"error": "No matching product found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response({"product": serializer.data}, status=status.HTTP_200_OK)
        # Optionally, you can cache the product details
        




# # Product Update View (PUT request for update)
# class ProductUpdateView(generics.UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def perform_update(self, serializer):
#         # Update the product object
#         product = serializer.save()
#         # Clear the cache for the user's product list
#         user = self.request.user
#         cache.delete(f'product_list_{user.id}')  # Clear cache when a product is updated
#         # Optionally, you can cache the updated product
#         cache.set(f'product_{product.id}', ProductSerializer(product).data, timeout=60*5)
#         return product

# # Product Destroy View (DELETE request to remove a product)
# class ProductDestroyView(generics.DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes=[IsAdminUser]

#     def perform_destroy(self, instance):
#         # Delete the product
#         instance.delete()
#         # Clear the cache for the user's product list
#         user = self.request.user
#         cache.delete(f'product_list_{user.id}')  # Clear cache when a product is deleted
#         return instance





class UpdateProductView(APIView):

    permission_classes=[IsAuthenticated,IsAdminUser]

    def put(self,request):

       #get the filter values 
        name = request.query_params.get('name')
        description = request.query_params.get('description')
        category = request.query_params.get('category')
        color = request.query_params.get('color')
        size = request.query_params.get('size')

        name = name.lower() if name else None
        description=description.lower() if description else None
        print(name)

        filters=Q()
        if name:
            filters &= Q(name__icontains=name)
        if description:
            filters &= Q(description__icontains=description)
        if category:
            filters &= Q(category__iexact=category)
        if color:
            filters &= Q(colors__name__iexact=color)
        if size:
            filters &= Q(sizes__name__iexact=size)

        #search product
        product = Product.objects.filter(filters).distinct().first()
        
        if not product:

            return Response({"error":"No matching product found"},status=status.HTTP_404_NOT_FOUND)
        

        serializer=ProductSerializer(product,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response({"product":serializer.data,"msg":"product updated successfully"},status=status.HTTP_200_OK)

        return Response({"error":serializer.errors,'msg':"something went wrong"})
    


#update product
class DeleteProductView(APIView):

    permission_classes=[IsAuthenticated,IsAdminUser]

    def delete(self,request):

       #get the filter values 
        name = request.query_params.get('name')
        description = request.query_params.get('description')
        category = request.query_params.get('category')
        color = request.query_params.get('color')
        size = request.query_params.get('size')

        name = name.lower() if name else None
        description=description.lower() if description else None

        filters=Q()
        if name:
            filters &= Q(name__icontains=name)
        if description:
            filters &= Q(description__icontains=description)
        if category:
            filters &= Q(category__iexact=category)
        if color:
            filters &= Q(colors__name__iexact=color)
        if size:
            filters &= Q(sizes__name__iexact=size)

        #search product
        product = Product.objects.filter(filters).distinct().first()
        
        if not product:

            return Response({"error":"No matching product found"},status=status.HTTP_404_NOT_FOUND)
        
        product.delete()

        return Response({"product":f"{name}","msg":"product deleted successfully"},status=status.HTTP_200_OK)


#updating macthicng prouduct
class UpdateMatchingProductsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request):
        name = request.query_params.get('name')
        description = request.query_params.get('description')
        category = request.query_params.get('category')
        color = request.query_params.get('color')
        size = request.query_params.get('size')

        name = name.lower() if name else None
        description = description.lower() if description else None

        filters = Q()
        if name:
            filters &= Q(name__icontains=name)
        if description:
            filters &= Q(description__icontains=description)
        if category:
            filters &= Q(category__iexact=category)
        if color:
            filters &= Q(colors__name__iexact=color)
        if size:
            filters &= Q(sizes__name__iexact=size)

        products = Product.objects.filter(filters).distinct()

        if not products.exists():
            return Response({"error": "No matching products found"}, status=status.HTTP_404_NOT_FOUND)

        updated_products = []
        errors = []

        for product in products:
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_products.append(serializer.data)
            else:
                errors.append({"product": product.name, "errors": serializer.errors})

        return Response({
            "updated": updated_products,
            "errors": errors,
            "msg": f"{len(updated_products)} product(s) updated"
        }, status=status.HTTP_200_OK)


#matching prouduct deletation
class DeleteMatchingProductsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request):
        # Fetch query parameters
        name = request.query_params.get('name', '').strip().lower()
        description = request.query_params.get('description', '').strip().lower()
        category = request.query_params.get('category')
        color = request.query_params.get('color')
        size = request.query_params.get('size')

        # Build filters
        filters = Q()
        if name:
            filters &= Q(name__icontains=name)
        if description:
            filters &= Q(description__icontains=description)
        if category:
            filters &= Q(category__iexact=category)
        if color:
            filters &= Q(colors__name__iexact=color)
        if size:
            filters &= Q(sizes__name__iexact=size)

        # Query matching products
        matching_products = Product.objects.filter(filters).distinct()

        if not matching_products.exists():
            return Response({"error": "No matching products found."}, status=status.HTTP_404_NOT_FOUND)

        deleted_count = matching_products.count()
        deleted_names = list(matching_products.values_list('name', flat=True))

        # Perform deletion
        matching_products.delete()

        return Response({
            "msg": f"Deleted {deleted_count} matching product(s).",
            "products_deleted": deleted_names
        }, status=status.HTTP_200_OK)
