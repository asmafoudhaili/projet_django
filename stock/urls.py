# perfumes/urls.py
from django.urls import path
from .views import stock_list, stock_add, stock_update, stock_delete

urlpatterns = [
    path('', stock_list, name='stock_list'),
    path('stocks/add/', stock_add, name='stock_add'),
    path('stocks/update/<int:pk>/', stock_update, name='stock_update'),
]
