from datetime import timedelta
from django.utils.timezone import now
from celery import shared_task
from orders.models import Order

@shared_task
def remove_expired_orders():
    expiration_time = now() - timedelta(hours=24)

    # Get all expired pending orders
    expired_orders = Order.objects.filter(status='pending', updated_at__lt=expiration_time)

    # Bulk update stock
    products_to_update = {}
    for order in expired_orders:
        for item in order.items.all():
            product = item.product
            if product in products_to_update:
                products_to_update[product] += item.quantity
            else:
                products_to_update[product] = item.quantity

    # Bulk update product stock
    for product, qty in products_to_update.items():
        product.stock += qty
        product.save(update_fields=['stock'])

    # Bulk delete expired orders
    expired_orders.delete()

    print(f"✅ Removed {expired_orders.count()} expired orders.")
