from datetime import timedelta
from django.utils.timezone import now
from celery import shared_task
from cart.models import CartItem

@shared_task
def remove_expired_cart_items():
    expiration_time = now() - timedelta(hours=24)

    # Get all expired cart items
    expired_items = CartItem.objects.filter(state='pending', updated_at__lt=expiration_time)

    # Bulk update stock
    products_to_update = {}
    for item in expired_items:
        product = item.product
        if product in products_to_update:
            products_to_update[product] += item.quantity
        else:
            products_to_update[product] = item.quantity

    # Bulk update product stock
    for product, qty in products_to_update.items():
        product.stock += qty
        product.save(update_fields=['stock'])

    # Bulk delete expired cart items
    expired_items.delete()

    print(f"✅ Removed {expired_items.count()} expired cart items.")
