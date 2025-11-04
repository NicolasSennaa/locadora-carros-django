from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Carro, Cliente, Aluguel

# 1. Home Page (TemplateView)
class HomeView(TemplateView):
    """Página inicial da Locadora."""
    template_name = 'carros/home.html'

# 2. Lista de Carros (ListView)
class CarroListView(ListView):
    """Lista todos os carros disponíveis."""
    model = Carro
    template_name = 'carros/carro_list.html'
    context_object_name = 'carros'
    # Ordena os carros por marca e modelo
    queryset = Carro.objects.all().order_by('marca', 'modelo') 

# 3. Detalhes do Carro (DetailView)
class CarroDetailView(DetailView):
    """Exibe detalhes de um carro específico."""
    model = Carro
    template_name = 'carros/carro_detail.html'
    context_object_name = 'carro'
    
    # Opcional: Adicionar lógica para exibir aluguéis relacionados no contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Busca os últimos 5 aluguéis relacionados a este carro
        context['ultimos_alugueis'] = Aluguel.objects.filter(carro=self.object).order_by('-data_inicio')[:5]
        return context

# 4. Lista de Clientes (ListView)
class ClienteListView(ListView):
    """Lista todos os clientes cadastrados."""
    model = Cliente
    template_name = 'carros/cliente_list.html'
    context_object_name = 'clientes'
    # Ordena os clientes por nome
    queryset = Cliente.objects.all().order_by('nome') 

# 5. Lista de Aluguéis (ListView)
class AluguelListView(ListView):
    """Lista todos os aluguéis registrados."""
    model = Aluguel
    template_name = 'carros/aluguel_list.html'
    context_object_name = 'alugueis'
    # Ordena os aluguéis pela data de início (mais recentes primeiro)
    queryset = Aluguel.objects.all().select_related('carro', 'cliente').order_by('-data_inicio')
