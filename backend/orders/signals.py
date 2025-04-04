from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now, timedelta
from orders.models import Order
from products.models import Product


# Restock products if an order is canceled
@receiver(post_save, sender=Order)
def restock_on_order_cancel(sender, instance, **kwargs):
    print("initaited the product increasing")
    if instance.status == 'cancelled':
        for item in instance.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
            print(f"product stock updated to{product.stock} action order  canceled")

    

#Automatically remove expired orders and restock items
# @receiver(post_save, sender=Order)
# def auto_remove_expired_orders(sender, instance, **kwargs):
#     expiration_time = now() - timedelta(hours=24)  # Set expiration to 24 hours
#     expired_orders = Order.objects.filter(status='pending', created_at__lt=expiration_time)
    
#     for order in expired_orders:
#         for item in order.items.all():
#             product = item.product
#             product.stock += item.quantity
#             product.save()
#         order.delete()
