from django.urls import path
from . import views

urlpatterns = [
    path('', views.trajet_list, name='trajet_list'),
    path('<int:pk>/', views.trajet_detail, name='trajet_detail'),
    path('ajouter/', views.trajet_create, name='trajet_create'),
    path('<int:pk>/modifier/', views.trajet_update, name='trajet_update'),
    path('<int:pk>/supprimer/', views.trajet_delete, name='trajet_delete'),
]
