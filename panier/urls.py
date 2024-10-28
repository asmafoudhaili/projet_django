from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_list, name='cart_view'),
    path('remove/<int:item_id>/', views.cart_remove_item, name='cart_remove_item'),
    path('update/<str:action>/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
]
