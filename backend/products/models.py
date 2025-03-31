from django.db import models

class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sizes = models.ForeignKey(Size, related_name='products',on_delete=models.CASCADE,null=True,blank=True)
    colors = models.ForeignKey(Color, related_name='products',on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Cloud storage later

    def __str__(self):
        return self.name