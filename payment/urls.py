from django.urls import path
from . import views

urlpatterns = [
  path('create-checkout-session/<int:commande_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment/success/', views.success_view, name='payment_success'),
    path('payment/cancel/', views.cancel_view, name='payment_cancel'),
]
