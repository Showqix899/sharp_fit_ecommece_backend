from django.urls import path
from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView, SizeListCreateView, ColorListCreateView

urlpatterns = [
    path('sizes/', SizeListCreateView.as_view(), name='size-list-create'),
    path('colors/', ColorListCreateView.as_view(), name='color-list-create'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
]
