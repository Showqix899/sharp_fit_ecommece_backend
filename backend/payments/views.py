# payments/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
import stripe
from django.conf import settings
from orders.models import Order
from .models import Payment

# Set your secret key for stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from notifications.tasks import send_notification_email

# Set up Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()

class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, order_id):
        user = request.user
        # Validate order and user (Ensure this order belongs to the authenticated user)
        try:
            order = get_object_or_404(Order, id=order_id, user=user,status="pending")
            payment = Payment.objects.create(user=user)
            print("found active order")
        except Order.DoesNotExist:
            print("no active order")
            return Response("no active order")

        try:
            # Create a payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),  # Stripe uses the smallest currency unit (cents)
                currency='usd',
                metadata={'order_id': order.id},
            )

            # Save the payment intent ID to the Payment model
            payment.stripe_payment_intent_id = payment_intent.id
            payment.amount = order.total_price
            payment.order = order
            payment.status = 'in_progress'
            payment.save()
            order.status="completed"
            order.save()


            return Response({'client_secret': payment_intent.client_secret}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any errors that occur during the payment intent creation
            # Log the error for debugging
            print("Error creating payment intent:", str(e))
            # You can also log the error to a logging service or send an email notification
            # Return an error response to the client
            payment.status = 'failed'
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




# # Confirm Payment View # This view will be called after the payment is confirmed on the client side
class ConfirmPaymentView(APIView):
    def post(self, request):
        payment_intent_id = request.data.get('payment_intent_id')

        # Retrieve the payment object from the database
        payment = get_object_or_404(Payment, stripe_payment_intent_id=payment_intent_id)

        try:
            # Retrieve the payment intent from Stripe
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Check the payment status
            if payment_intent.status == 'succeeded':
                payment.status = 'completed'
                payment.save()
                notification=Notification.objects.create(
                    user=payment.user,
                    title="Payment Successful",
                    message=f"Your payment for order {payment.order.id} was successful."
                )
                # Send email notification asynchronously using Celery
                subject = "Payment Confirmation"
                message = f"Dear {payment.user.email},\n\nYour payment for Order #{payment.order.id} was successful."
                send_notification_email.delay(payment.user.email, subject, message)
                print("Payment successful notification sent.")
                return JsonResponse({'message': 'Payment confirmed successfully'})
            else:
                return JsonResponse({'message': 'Payment failed'}, status=400)

        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)
