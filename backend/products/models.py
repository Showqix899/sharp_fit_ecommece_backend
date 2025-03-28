# from django.db import models

# class Size(models.Model):
#     name = models.CharField(max_length=20, unique=True)

#     def __str__(self):
#         return self.name

# class Color(models.Model):
#     name = models.CharField(max_length=30, unique=True)

#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='product_images/')
#     sizes = models.ManyToManyField(Size, blank=True)
#     colors = models.ManyToManyField(Color, blank=True)

#     def __str__(self):
#         return self.name
