# commande_perso/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('customization-options/', views.customization_option_list, name='customization_option_list'),
    path('customization-options/new/', views.customization_option_create, name='customization_option_create'),
    path('customization-options/<int:pk>/edit/', views.customization_option_update, name='customization_option_update'),
    path('customization-options/<int:pk>/delete/', views.customization_option_delete, name='customization_option_delete'),

    path('custom-orders/', views.custom_order_list, name='custom_order_list'),
    path('custom-orders/new/', views.custom_order_create, name='custom_order_create'),
    path('custom-orders/<int:pk>/edit/', views.custom_order_update, name='custom_order_update'),
    path('custom-orders/<int:pk>/delete/', views.custom_order_delete, name='custom_order_delete'),

    path('guide/', views.guide_view, name='guide'),  # Ajoutez cette ligne pour la route du guide
]
