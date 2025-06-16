from django.db import models
from cloudinary.models import CloudinaryField


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('shirt', 'Shirt'),
        ('pant', 'Pant'),
        ('underwear', 'Underwear'),
        ('t_shirt', 'T-Shirt'),
        ('polo_shirt', 'Polo Shirt'),
        ('combo', 'Combo'),
        ('trouser', 'Trouser'),
        ('shock', 'Shock'),
        ('muffler', 'Muffler'),
        ('full_sleeve_shirt', 'Full Sleeve Shirt'),
        ('jacket', 'Jacket'),
        ('sweater', 'Sweater'),
        ('huddy', 'Huddy'),
        ('cargo_shorts', 'Cargo Shorts'),
        ('jersey', 'Jersey'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='shirt',  # Default to 'shirt'
    )

    sizes = models.ManyToManyField(Size, related_name='products', blank=True)
    colors = models.ManyToManyField(Color, related_name='products', blank=True)
    image = CloudinaryField("product_image",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return self.name
