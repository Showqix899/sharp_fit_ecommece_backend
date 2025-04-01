# payments/urls.py
from django.urls import path
from .views import CreatePaymentIntentView, ConfirmPaymentView

urlpatterns = [
    path('payments/create_payment_intent/<int:order_id>/', CreatePaymentIntentView.as_view(), name='create_payment_intent'),
    path('confirm_payment/', ConfirmPaymentView.as_view(), name='confirm_payment'),
]
