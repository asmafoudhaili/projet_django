from django.urls import path
from . import views

urlpatterns = [
    path('', views.livraison_list, name='livraison_list'),
    path('<int:pk>/', views.livraison_detail, name='livraison_detail'),
    path('ajouter/', views.livraison_create, name='livraison_create'),
    path('<int:pk>/modifier/', views.livraison_update, name='livraison_update'),
    path('<int:pk>/supprimer/', views.livraison_delete, name='livraison_delete'),
]
