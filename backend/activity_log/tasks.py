from products.models import Product, Size, Color
from orders.models import Order
from .models import ActivityLog
from payments.models import Payment
from cart.models import Cart
from users.models import CustomUser
from celery import shared_task
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


from django.dispatch import Signal
user_logged_in_custom = Signal()

@shared_task
def user_log_activity(user_id, action, details):
    try:
        user = CustomUser.objects.filter(id=user_id).first()
        if user:
            ActivityLog.objects.create(
                user=user,
                action=action,
                details=details,
                timestamp=timezone.now()
            )
            print(f"Activity logged: {action} - {details}")
        else:
            pass
    except Exception as e:
        pass


@shared_task
def custom_login_activity(user_id,action,details):

    try:
        user=CustomUser.objects.filter(id=user_id).first()

        if user:
            ActivityLog.objects.create(
                user=user,
                action=action,
                details=details,
                timestamp=timezone.now()
            )
            print(f'activity logged: {action} - {details}')
        else:
            print("user not found")
    except Exception as e:
        print("error")


@shared_task
def log_activity(instance_id, action, details):
    try:
        if isinstance(details, dict):
            model = details.get('model')
            instance = None
            if model == 'Product':
                instance = Product.objects.filter(id=instance_id).first()
            elif model == 'Order':
                instance = Order.objects.filter(id=instance_id).first()
            elif model == 'Payment':
                instance = Payment.objects.filter(id=instance_id).first()
            elif model == 'Cart':
                instance = Cart.objects.filter(id=instance_id).first()
            elif model == 'Size':
                instance = Size.objects.filter(id=instance_id).first()
            elif model == 'Color':
                instance = Color.objects.filter(id=instance_id).first()

            user = instance.user if hasattr(instance, 'user') else None
            log=ActivityLog.objects.create(
                user=user,
                action=action,
                details=details,
                timestamp=timezone.now()
            )
            log.save()
    except Exception as e:
        print(f"Error logging activity: {e}")


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    
    user_ip = request.META.get('REMOTE_ADDR', 'Unknown IP')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown Device')
    user=request.user
    user_log_activity.delay(
        user.id,
        "User Logged In",
        {"ip": user_ip, "user_agent": user_agent}
    )
    print("User logged in:", user.email)


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    user_ip = request.META.get('REMOTE_ADDR', 'Unknown IP')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown Device')
    user_log_activity.delay(
        user.id,
        "User Logged Out",
        {"ip": user_ip, "user_agent": user_agent}
    )


@receiver(post_save, sender=CustomUser)
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        user_log_activity.delay(
            instance.id,
            "User Created",
            {"username": instance.email, "email": instance.email}
        )


@receiver(post_delete, sender=CustomUser)
def log_user_deletion(sender, instance, **kwargs):
    user_log_activity.delay(
        instance.id,
        "User Deleted",
        {"username": instance.email, "email": instance.email}
    )


@receiver(pre_save, sender=CustomUser)
def log_user_update(sender, instance, **kwargs):
    if instance.pk:
        original_instance = CustomUser.objects.get(pk=instance.pk)
        changes = {}
        if original_instance.email != instance.email:
            changes['email'] = (original_instance.email, instance.email)
        if changes:
            user_log_activity.delay(
                instance.id,
                "User Updated",
                changes
            )


@receiver(post_save, sender=Product)
def log_product_creation(sender, instance, created, **kwargs):
    if created:
        log_activity.delay(
            instance.id,
            "Product Created",
            {"name": instance.name, "price": str(instance.price), "model": "Product"}
        )


@receiver(pre_save, sender=Product)
def log_product_update(sender, instance, **kwargs):
    if instance.pk:
        original_instance = Product.objects.get(pk=instance.pk)
        changes = {}
        if original_instance.name != instance.name:
            changes['name'] = (original_instance.name, instance.name)
        if original_instance.price != instance.price:
            changes['price'] = (str(original_instance.price), str(instance.price))
        if changes:
            log_activity.delay(
                instance.id,
                "Product Updated",
                {"changes": changes, "model": "Product"}
            )


@receiver(post_delete, sender=Product)
def log_product_deletion(sender, instance, **kwargs):
    log_activity.delay(
        instance.id,
        "Product Deleted",
        {"name": instance.name, "price": str(instance.price), "model": "Product"}
    )


@receiver(post_save, sender=Order)
def log_order_creation(sender, instance, created, **kwargs):
    if created:
        log_activity.delay(
            instance.id,
            "Order Created",
            {"user": instance.user.email, "total": str(instance.total_price), "model": "Order"}
        )


@receiver(pre_save, sender=Order)
def log_order_update(sender, instance, **kwargs):
    if instance.pk:
        original_instance = Order.objects.get(pk=instance.pk)
        changes = {}
        if original_instance.status != instance.status:
            changes['status'] = (original_instance.status, instance.status)
        if changes:
            log_activity.delay(
                instance.id,
                "Order Updated",
                {"changes": changes, "model": "Order"}
            )


@receiver(post_delete, sender=Order)
def log_order_deletion(sender, instance, **kwargs):
    log_activity.delay(
        instance.id,
        "Order Deleted",
        {"user": instance.user.email, "total": str(instance.total_price), "model": "Order"}
    )


@receiver(post_save, sender=Payment)
def log_payment_creation(sender, instance, created, **kwargs):
    if created:
        log_activity.delay(
            instance.id,
            "Payment Created",
            {"order_id": instance.order.id, "amount": str(instance.amount), "model": "Payment"}
        )


@receiver(pre_save, sender=Payment)
def log_payment_update(sender, instance, **kwargs):
    if instance.pk:
        original_instance = Payment.objects.get(pk=instance.pk)
        changes = {}
        if original_instance.amount != instance.amount:
            changes['amount'] = (str(original_instance.amount), str(instance.amount))
        if changes:
            log_activity.delay(
                instance.id,
                "Payment Updated",
                {"changes": changes, "model": "Payment"}
            )


@receiver(post_delete, sender=Payment)
def log_payment_deletion(sender, instance, **kwargs):
    log_activity.delay(
        instance.id,
        "Payment Deleted",
        {"order_id": instance.order.id, "amount": str(instance.amount), "model": "Payment"}
    )


@receiver(post_save, sender=Cart)
def log_cart_creation(sender, instance, created, **kwargs):
    if created:
        log_activity.delay(
            instance.id,
            "Cart Created",
            {"user": instance.user.email, "model": "Cart"}
        )


@receiver(pre_save, sender=Cart)
def log_cart_update(sender, instance, **kwargs):
    if instance.pk:
        original_instance = Cart.objects.get(pk=instance.pk)
        changes = {}
        if original_instance.items != instance.items:
            changes['items'] = (original_instance.items, instance.items)
        if changes:
            log_activity.delay(
                instance.id,
                "Cart Updated",
                {"changes": changes, "model": "Cart"}
            )


@receiver(post_delete, sender=Cart)
def log_cart_deletion(sender, instance, **kwargs):
    log_activity.delay(
        instance.id,
        "Cart Deleted",
        {"user": instance.user.email, "model": "Cart"}
    )


@receiver(post_save, sender=Size)
def log_size_creation(sender, instance, created, **kwargs):
    if created:
        log_activity.delay(
            instance.id,
            "Size Created",
            {"name": instance.name, "model": "Size"}
        )


@receiver(pre_save, sender=Size)
def log_size_update(sender, instance, **kwargs):
    if instance.pk:
        original_instance = Size.objects.get(pk=instance.pk)
        changes = {}
        if original_instance.name != instance.name:
            changes['name'] = (original_instance.name, instance.name)
        if changes:
            log_activity.delay(
                instance.id,
                "Size Updated",
                {"changes": changes, "model": "Size"}
            )


@receiver(post_delete, sender=Size)
def log_size_deletion(sender, instance, **kwargs):
    log_activity.delay(
        instance.id,
        "Size Deleted",
        {"name": instance.name, "model": "Size"}
    )


@receiver(post_save, sender=Color)
def log_color_creation(sender, instance, created, **kwargs):
    if created:
        log_activity.delay(
            instance.id,
            "Color Created",
            {"name": instance.name, "model": "Color"}
        )


@receiver(pre_save, sender=Color)
def log_color_update(sender, instance, **kwargs):
    if instance.pk:
        original_instance = Color.objects.get(pk=instance.pk)
        changes = {}
        if original_instance.name != instance.name:
            changes['name'] = (original_instance.name, instance.name)
        if changes:
            log_activity.delay(
                instance.id,
                "Color Updated",
                {"changes": changes, "model": "Color"}
            )


@receiver(post_delete, sender=Color)
def log_color_deletion(sender, instance, **kwargs):
    log_activity.delay(
        instance.id,
        "Color Deleted",
        {"name": instance.name, "model": "Color"}
    )
