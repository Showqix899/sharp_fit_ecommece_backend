from django.urls import path
from .views import (
    SizeListCreateView,
    ColorListCreateView,
    ProductListCreateView,
    ProductCreateView,
    ProductRetrieveView,
    # ProductUpdateView,
    # ProductDestroyView
    UpdateMatchingProductsView,
    DeleteMatchingProductsView,
    UpdateProductView,
    DeleteProductView,


)

urlpatterns = [
    # Size URLs
    path('sizes/create/', SizeListCreateView.as_view(), name='size-list-create'),

    # Color URLs
    path('colors/', ColorListCreateView.as_view(), name='color-list-create'),

    # Product URLs
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('', ProductRetrieveView.as_view(), name='product-retrieve'),
    # path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    # path('products/<int:pk>/delete/', ProductDestroyView.as_view(), name='product-delete'),
    path('delete/', DeleteProductView.as_view(), name='product-delete'),
    path('update/', UpdateProductView.as_view(), name='product-update'),
    path('update-matching-products/', UpdateMatchingProductsView.as_view(), name='update-matching-products'),
    path('delete-matching-products/', DeleteMatchingProductsView.as_view(), name='delete-matching-products'),

]
