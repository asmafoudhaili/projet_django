from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_list, name='cart_view'),
    path('remove/<int:item_id>/', views.cart_remove_item, name='cart_remove_item'),
    path('update/<str:action>/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('delete-commande/<int:commande_id>/', views.delete_commande, name='delete_commande'),

    
]
