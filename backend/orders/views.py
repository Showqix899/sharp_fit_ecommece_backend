from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListAPIView


from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator




from .models import Order, OrderItem
from cart.models import Cart, CartItem
from .serializers import OrderSerializer


#for sending notification 
from notifications.tasks import send_notification_email
from notifications.models import Notification



#create order view
class CreateOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, status='active').first()

        if not cart:
            return Response({'message': 'No active cart found'}, status=status.HTTP_400_BAD_REQUEST)

        # Create Order
        order = Order.objects.create(user=user, total_price=0)

        order_total = 0
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                size=cart_item.size,
                color=cart_item.color,
                quantity=cart_item.quantity,
                subtotal=cart_item.subtotal
            )
            order_total += cart_item.subtotal

        order.total_price = order_total
        order.save()

        #order cache updation
        cache.delete(f'order_{user.id}')



        # Clear the cart
        cart.items.all().delete()
        cart.status = 'checked_out'
        cart.save()


        return Response({'message': 'Order created successfully', 'order_id': order.id,'user':order.user.email,'order_total':order_total}, status=status.HTTP_201_CREATED)

#order list view
class OrderListView(ListAPIView):

    permission_classes=[IsAuthenticated]
    

    def get(self, request):
        user= request.user
        cache_key = f'order_{user.id}'
        order_response=cache.get(cache_key)
        if not order_response:
            orders = Order.objects.filter(user=user).order_by('-created_at')
            serializer = OrderSerializer(orders, many=True)
            order_response = serializer.data
            # Cache the order response for 5 minutes
            cache.set(cache_key, order_response, timeout=60*5)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(order_response, status=status.HTTP_200_OK)
        



#get order details view
class OrderDetailView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, order_id):
        user = request.user
        order = get_object_or_404(Order, id=order_id, user=user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


#cancel order view
class CancelOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        user = request.user
        order = get_object_or_404(Order, id=order_id, user=user)

        if order.status in ['shipped', 'delivered']:
            return Response({'message': 'Order cannot be canceled after it is shipped/delivered'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'cancelled'
        order.save()

        # Update the cache
        cache.delete(f'order_{user.id}')

        
        
        # Send notification email
        user_email = user.email
        message= f"Your order {order.id} has been canceled."
        subject = "Order Cancellation Notice"

        # Create a notification record
        notification= Notification.objects.create(
            user=user,
            title="Order Canceled",
            message=message
        )

        notification.save()
        
        
        # Send email notification asynchronously using Celery
        send_notification_email.delay(user_email, subject, message)

        return Response({'message': 'Order canceled successfully'}, status=status.HTTP_200_OK)
    



#for admin to get all the orders
class AdminOrderListView(APIView):
    
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)