from django.urls import path
from . import views
from perfumes.views import description_create, description_update ,description_delete # Ensure description_update is imported
from .views import description_list
urlpatterns=[
    path('',views.index,name='index'),
    path('descriptions/', description_list, name='description_list'),
    path('descriptions/create/', description_create, name='description_create'),
    path('descriptions/update/<int:id>/', description_update, name='description_update'),
    path('descriptions/delete/<int:pk>/', description_delete, name='description_delete'),
    path('order/', views.order_perfume, name='order_perfume'),

]