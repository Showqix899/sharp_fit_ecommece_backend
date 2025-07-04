from django.contrib import admin
from django.urls import path, include
from activity_log.views import list_log

from django.conf import settings
from django.conf.urls.static import static



#swagger configuration
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('product/', include('products.urls')),
    path('order/',include('orders.urls')),
    path('cart/', include('cart.urls')),
    path('payment/',include('payments.urls')),
    path('logs/',list_log.as_view(),name='list_log'),
    path('admin/',include('admincontroll.urls')),

    #swagger url
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    

]

