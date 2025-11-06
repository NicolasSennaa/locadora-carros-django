from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Carro, Cliente, Aluguel

# Home Page (TemplateView)
class HomeView(TemplateView):
    """Página inicial da Locadora."""
    template_name = 'carros/home.html'

# Lista de Carros (ListView)
class CarroListView(ListView):
    """Lista todos os carros disponíveis."""
    model = Carro
    template_name = 'carros/carro_list.html'
    context_object_name = 'carros'
    queryset = Carro.objects.all().order_by('marca', 'modelo') 

# Detalhes do Carro (DetailView)
class CarroDetailView(DetailView):
    """Exibe detalhes de um carro específico."""
    model = Carro
    template_name = 'carros/carro_detail.html'
    context_object_name = 'carro'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimos_alugueis'] = Aluguel.objects.filter(carro=self.object).order_by('-data_inicio')[:5]
        return context

# Lista de Clientes (ListView)
class ClienteListView(ListView):
    """Lista todos os clientes cadastrados."""
    model = Cliente
    template_name = 'carros/cliente_list.html'
    context_object_name = 'clientes'
    # Ordena os clientes por nome
    queryset = Cliente.objects.all().order_by('nome') 

# Lista de Aluguéis (ListView)
class AluguelListView(ListView):
    """Lista todos os aluguéis registrados."""
    model = Aluguel
    template_name = 'carros/aluguel_list.html'
    context_object_name = 'alugueis'
    queryset = Aluguel.objects.all().select_related('carro', 'cliente').order_by('-data_inicio')
    
# View de Cadastro de Usuário (Registro)
class RegisterView(CreateView):
    """Permite que novos usuários se cadastrem."""
    form_class = UserCreationForm
    success_url = reverse_lazy('login') 
    template_name = 'registration/register.html'