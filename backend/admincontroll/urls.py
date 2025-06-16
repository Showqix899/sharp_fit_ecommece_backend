from django.urls import path
from .views import (
    AdminUserDeleteView,AdminUserUpdateView,
    generate_admin_invite,ListOfAdmin,ListOfUsers,
    UserDetailsView,UpdateProductView,DeleteProductView,
    UpdateMatchingProductsView,DeleteMatchingProductsView,
    OrderListAdminView,

)

from products.views import ProductCreateView


urlpatterns = [

    #user
    path('users/update/', AdminUserUpdateView.as_view(), name='admin-user-update'),
    path('users/delete/', AdminUserDeleteView.as_view(), name='admin-user-delete'),
    path('invite/',generate_admin_invite,name='admin-invite'),
    path('admin-list/',ListOfAdmin.as_view(),name='admin-list'),
    path('user-list/',ListOfUsers.as_view(),name='user-list'),
    path('user-details/',UserDetailsView.as_view(),name="user-details"),
    #product
    path('product/create/',ProductCreateView.as_view(),name='product-create'),
    path('update/product/',UpdateProductView.as_view(),name='product-update'),
    path('product/delete/',DeleteProductView.as_view(),name="product-delete"),
    path('matching-product-updation/',UpdateMatchingProductsView.as_view(),name='update-matching-prouduct'),
    path('matching-product-deletation/',DeleteMatchingProductsView.as_view(),name='delete-matching-prouduct'),

    #order
    path('order/list/',OrderListAdminView.as_view(),name='admin-order-list'),

]

