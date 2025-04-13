from django.urls import path
from .views import (
    AdminUserDeleteView,AdminUserUpdateView,
    generate_admin_invite,ListOfAdmin,ListOfUsers,
    UserDetailsView,UpdateProductView,DeleteProductView

)




urlpatterns = [
    path('admin/users/update/', AdminUserUpdateView.as_view(), name='admin-user-update'),
    path('admin/users/delete/', AdminUserDeleteView.as_view(), name='admin-user-delete'),
    path('admin/invite/',generate_admin_invite,name='admin-invite'),
    path('admin/admin-list/',ListOfAdmin.as_view(),name='admin-list'),
    path('admin/user-list/',ListOfUsers.as_view(),name='user-list'),
    path('admin/user-details/',UserDetailsView.as_view(),name="user-details"),
    path('admin/update-product/',UpdateProductView.as_view(),name='product-update'),
    path('admin/product/delete/',DeleteProductView.as_view(),name="product-delete"),
]

