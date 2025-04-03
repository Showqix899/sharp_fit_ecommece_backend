from django.db.models.signals import post_save,post_delete,pre_delete
from django.dispatch import receiver
from django.utils.timezone import now, timedelta
from cart.models import CartItem, Cart
from products.models import Product


# Reduce stock when a CartItem is added or updated
@receiver(post_save, sender=CartItem)
def update_stock_on_cart_add(sender, instance, created, **kwargs):
    if created or instance.quantity:  # Ensure only valid updates
        product = instance.product
        product.stock = max(0, product.stock - instance.quantity)  # Prevent negative stock
        product.save()
        print(f"product stock updated to{product.stock} action cartitem created")

# Restock when a CartItem is deleted
@receiver(post_delete, sender=CartItem)
def restock_on_cart_remove(sender, instance, **kwargs):
    if instance.state =="canceled":
        product = instance.product
        product.stock += instance.quantity
        product.save()
        print(f'product stock updated to {product.stock} action -> cart item removed')



# #automatic deletation after creating a cart item
# @receiver(post_save, sender=CartItem)
# def auto_remove_expired_cart_items(sender, instance, created, **kwargs):
#     # Check if it's not a new object (i.e., it's an update)
#     if created:
#         return  # Don't trigger deletion when it's first created.

#     # After creation, check expiration based on updated_at
#     expiration_time = now() - timedelta(hours=24)  # 24-hour expiration
#     if instance.state == 'pending' and instance.updated_at < expiration_time:
#         product = instance.product
#         product.stock += instance.quantity
#         product.save()
#         instance.delete()

#     print("Expired cart items removed successfully.")




