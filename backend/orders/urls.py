from django.urls import path
from .views import CreateOrderView, OrderListView, OrderDetailView, CancelOrderView,AdminOrderListView 

urlpatterns = [
    path('orders/create/', CreateOrderView.as_view(), name='order-create'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/cancel/', CancelOrderView.as_view(), name='order-cancel'),
    path('admin/orders-list/',AdminOrderListView.as_view(), name='admin-order-list'),
]