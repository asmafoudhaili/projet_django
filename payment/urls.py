from django.urls import path
from . import views

urlpatterns = [
    path('commande/<int:commande_id>/', views.commande_detail, name='commande_detail'),
    path('create-checkout-session/<int:commande_id>/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('prediction/', views.display_revenue_prediction, name='prediction'),

]
