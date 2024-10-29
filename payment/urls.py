from django.urls import path
from . import views

urlpatterns = [
    path('commande/<int:commande_id>/', views.commande_detail, name='commande_detail'),
    path('prediction/', views.display_revenue_prediction, name='prediction'),

]
