from django.urls import path
from .views import HomeView, CarroListView, CarroDetailView, ClienteListView, AluguelListView

app_name = 'carros'

urlpatterns = [
    # 1. Página Home
    path('', HomeView.as_view(), name='home'), 
    
    # 2. Lista de Carros
    path('carros/', CarroListView.as_view(), name='lista_carros'), 
    
    # 3. Detalhes do Carro (pk = primary key)
    path('carros/<int:pk>/', CarroDetailView.as_view(), name='detalhe_carro'), 
    
    # 4. Lista de Clientes
    path('clientes/', ClienteListView.as_view(), name='lista_clientes'), 
    
    # 5. Lista de Aluguéis
    path('alugueis/', AluguelListView.as_view(), name='lista_alugueis'), 
]