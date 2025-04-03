# models.py in the cart app
from django.db import models
from django.conf import settings
from products.models import Product
from django.contrib.auth import get_user_model

User= get_user_model()


class Cart(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('checked_out', 'Checked Out'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user.email}"

    def total_price(self):
        """
        Calculate the total price of the cart by summing up the subtotals of all CartItems.
        """
        total = sum(item.subtotal for item in self.items.all())  # 'items' is the related name
        return total

    def total_items(self):
        """
        Calculate the total number of items in the cart (sum of quantities).
        """
        total = sum(item.quantity for item in self.items.all())  # 'items' is the related name
        return total


class CartItem(models.Model):

    STATUS_CHOICES=[
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('canceled','Canceled')
    ]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, null=True, blank=True)  # Added size field
    color = models.CharField(max_length=20, null=True, blank=True)  # Added color field
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    state=models.CharField(max_length=20,null=True,blank=True,choices=STATUS_CHOICES,default='pending')
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        unique_together = ('cart', 'product', 'size', 'color')  # Ensures uniqueness of same product variation

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically update the subtotal when the CartItem is saved.
        """
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"
