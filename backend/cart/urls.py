from django.urls import path
from .views import CartDetailView, AddToCartView, RemoveFromCartView, UpdateCartView, CartListView

urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/update/', UpdateCartView.as_view(), name='update-cart'),
    path('cart/list/', CartListView.as_view(), name='cart-list')  # For admin use
]
