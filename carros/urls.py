from django.urls import path
from .views import (
    CarroListView, 
    CarroDetailView, 
    ClienteListView, 
    AluguelListView
)

app_name = 'carros'

urlpatterns = [
    # Carros
    path('lista/', CarroListView.as_view(), name='carro_list'),
    path('detalhe/<int:pk>/', CarroDetailView.as_view(), name='carro_detail'),

    # Clientes
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),

    # Aluguéis
    path('alugueis/', AluguelListView.as_view(), name='aluguel_list'),
]