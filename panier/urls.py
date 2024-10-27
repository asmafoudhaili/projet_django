from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_list, name='cart_view'),  # Vue principale du panier
    path('cart/item-count/', views.cart_item_count, name='cart_item_count'),

]
