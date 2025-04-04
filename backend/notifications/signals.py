from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from payments.models import Payment
from .models import Notification
from .tasks import send_notification_email



#if the order is cancel led, create a notification and send an email
# @receiver(post_save, sender=Order)
# def order_cancel_notification(sender, instance, created, **kwargs):
#     if instance.status == "cancelled":
#         # Create a notification record
#         Notification.objects.create(
#             user=instance.user,
#             title="Order Canceled",
#             message=f"Your order {instance.id} has been canceled."
#         )

#         # Send email notification asynchronously using Celery
#         subject = "Order Cancellation Notice"
#         message = f"Dear {instance.user.username},\n\nYour order #{instance.id} has been canceled."
#         send_email_notification.delay(instance.user.email, subject, message)
#         print("Order canceled notification sent.")



# If the order is completed, create a notification and send an email
@receiver(post_save, sender=Payment)
def payment_failure_notification(sender, instance, created, **kwargs):
    if instance.status == "failed":
        # Create a notification record
        Notification.objects.create(
            user=instance.user,
            title="Payment Failed",
            message=f"Your payment for order {instance.order.id} has failed."
        )

        # Send email notification asynchronously using Celery
        subject = "Payment Failure Alert"
        message = f"Dear {instance.user.username},\n\nYour payment for Order #{instance.order.id} has failed. Please try again."
        send_notification_email.delay(instance.user.email, subject, message)

        print("Payment failed notification sent.")


# If the payment is successful, create a notification and send an email
@receiver(post_save, sender=Payment)
def payment_success_notification(sender,instance,created,**kwargs):
    if instance.status == "completed":
        # Create a notification record
        Notification.objects.create(
            user=instance.user,
            title="Payment Successful",
            message=f"Your payment for order {instance.order.id} was successful."
        )

        # Send email notification asynchronously using Celery
        subject = "Payment Confirmation"
        message = f"Dear {instance.user.username},\n\nYour payment for Order #{instance.order.id} was successful."
        send_notification_email.delay(instance.user.email, subject, message)

        print("Payment successful notification sent.")
