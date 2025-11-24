from django.urls import path
from .views import (
    home_dispatch_view,         
    DashboardColaboradorView,
    CarroListView, 
    ClienteListView, 
    AluguelListView,
    HomeClienteView,             
    CarroDetailView,            
    alugar_carro_view,           
    aluguel_success_view,        
)

app_name = 'carros'

urlpatterns = [
    path('', home_dispatch_view, name='home'),
    path('dashboard/', DashboardColaboradorView.as_view(), name='home_colaborador'),
    path('lista/', CarroListView.as_view(), name='carro_list'),
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('alugueis/', AluguelListView.as_view(), name='aluguel_list'),
    path('home_cliente/', HomeClienteView.as_view(), name='home_cliente'),
    path('detalhe/<int:pk>/', CarroDetailView.as_view(), name='carro_detail'),
    path('alugar/<int:pk>/confirmar/', alugar_carro_view, name='alugar_carro'),
    path('aluguel/sucesso/', aluguel_success_view, name='aluguel_success'),
]