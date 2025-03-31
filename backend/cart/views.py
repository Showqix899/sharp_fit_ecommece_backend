from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from products.models import Product
from rest_framework.permissions import AllowAny
from .models import Cart, CartItem
from .serializers import CartSerializer, AddToCartSerializer, RemoveFromCartSerializer

class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user, status='active')
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            size = serializer.validated_data['size']
            color = serializer.validated_data['color']
            quantity = serializer.validated_data['quantity']

            product = Product.objects.get(id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user, status='active')

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product,size=size,color=color,defaults={'quantity':quantity})

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response({"message": f"{product.name} (Size:{size}, Color:{color}) added to the cart."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RemoveFromCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            cart = Cart.objects.filter(user=request.user, status='active').first()

            if not cart:
                return Response({"message": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

            if cart_item:
                cart_item.delete()
                return Response({"message": "Product removed from the cart."}, status=status.HTTP_200_OK)
            return Response({"message": "Product not found in the cart."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            cart, created = Cart.objects.get_or_create(user=request.user, status='active')
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

            if cart_item:
                cart_item.quantity = quantity
                cart_item.save()
                return Response({"message": f"Quantity of {cart_item.product.name} updated to {quantity}."}, status=status.HTTP_200_OK)
            return Response({"message": "Product not found in the cart."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartListView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
