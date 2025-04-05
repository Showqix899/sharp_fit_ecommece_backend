from django.urls import path
from .views import (
    SizeListCreateView,
    ColorListCreateView,
    ProductListCreateView,
    ProductCreateView,
    ProductRetrieveView,
    ProductUpdateView,
    ProductDestroyView
)

urlpatterns = [
    # Size URLs
    path('sizes/', SizeListCreateView.as_view(), name='size-list-create'),

    # Color URLs
    path('colors/', ColorListCreateView.as_view(), name='color-list-create'),

    # Product URLs
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductRetrieveView.as_view(), name='product-retrieve'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDestroyView.as_view(), name='product-delete'),
]
