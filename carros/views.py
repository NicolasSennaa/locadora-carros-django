from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.db import transaction 
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Carro, Cliente, Aluguel, Colaborador
from .forms import ClienteRegisterForm, AluguelForm

#  Mixins de Permissão

class ColaboradorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return hasattr(self.request.user, 'colaborador')

class ClienteRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'cliente')

# Views de Autenticação e Redirecionamento 

@login_required
def home_dispatch_view(request):
    """
    Redireciona o usuário para a home correta (Cliente ou Colaborador)
    após o login, baseado no seu perfil.
    """
    if hasattr(request.user, 'colaborador') or request.user.is_superuser:
        return redirect(reverse_lazy('carros:home_colaborador'))
    elif hasattr(request.user, 'cliente'):
        return redirect(reverse_lazy('carros:home_cliente'))
    else:
        return redirect(reverse_lazy('login'))

class ClienteRegisterView(CreateView):
    """
    View para registrar um novo Cliente, usando o formulário customizado.
    """
    form_class = ClienteRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        return super().form_valid(form)


#  Views do Colaborador (Gestão) 

class DashboardColaboradorView(ColaboradorRequiredMixin, TemplateView):
    """
    Página inicial do Colaborador (Dashboard com métricas).
    """
    template_name = 'carros/home_colaborador.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_carros'] = Carro.objects.count()
        context['total_clientes'] = Cliente.objects.count()
        context['alugueis_ativos'] = Aluguel.objects.filter(data_devolucao__isnull=True).count()
        return context

class CarroListView(ColaboradorRequiredMixin, ListView):
    """
    Lista todos os carros (acesso Colaborador). O link de ação deve apontar
    diretamente para a edição no Django Admin.
    """
    model = Carro
    template_name = 'carros/carro_list.html'
    context_object_name = 'carros'
    queryset = Carro.objects.all().order_by('marca', 'modelo')

class ClienteListView(ColaboradorRequiredMixin, ListView):
    """Lista todos os clientes (acesso Colaborador)."""
    model = Cliente
    template_name = 'carros/cliente_list.html'
    context_object_name = 'clientes'
    queryset = Cliente.objects.select_related('user').all().order_by('user__first_name')

class AluguelListView(ColaboradorRequiredMixin, ListView):
    """Lista todos os aluguéis (acesso Colaborador)."""
    model = Aluguel
    template_name = 'carros/aluguel_list.html'
    context_object_name = 'alugueis'
    queryset = Aluguel.objects.select_related('carro', 'cliente').all().order_by('-data_inicio')


#  Views do Cliente (Operação)

class HomeClienteView(ClienteRequiredMixin, ListView):
    """
    Página inicial do Cliente. Lista os carros disponíveis para alugar
    e exibe os aluguéis ativos e o histórico do cliente.
    """
    model = Carro
    template_name = 'carros/home_cliente.html'
    context_object_name = 'carros_disponiveis'
    
    def get_queryset(self):
        return Carro.objects.filter(disponivel=True).order_by('marca', 'modelo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        alugueis = Aluguel.objects.filter(cliente=user).select_related('carro').order_by('-data_inicio')
        
        context['alugueis_ativos'] = alugueis.filter(data_devolucao__isnull=True)
        context['historico_alugueis'] = alugueis.filter(data_devolucao__isnull=False)
        
        return context

class CarroDetailView(ClienteRequiredMixin, DetailView):
    """
    View de detalhe do carro para o cliente, incluindo o formulário de aluguel.
    """
    model = Carro
    template_name = 'carros/carro_detail.html' 
    context_object_name = 'carro'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AluguelForm(carro=self.object)
        return context

@login_required
def alugar_carro_view(request, pk):

    carro = get_object_or_404(Carro, pk=pk)
    
    if not carro.disponivel:
        messages.error(request, "Este carro não está disponível para aluguel no momento.")
        return redirect(reverse('carros:carro_detail', kwargs={'pk': carro.pk}))

    if request.method == 'POST':
        form = AluguelForm(request.POST, carro=carro)

        if form.is_valid():
            with transaction.atomic():
                aluguel = form.save(commit=False)
                
                try:
                    request.user.cliente 
                except Cliente.DoesNotExist:
                    messages.error(request, "Você precisa completar seu perfil de Cliente para alugar um carro.")
                    return redirect(reverse_lazy('login')) 
                    
                aluguel.cliente = request.user 
                
                aluguel.carro = carro
                
                aluguel.save()
                
                carro.disponivel = False
                carro.save()
                
                messages.success(request, f"Carro {carro.modelo} alugado com sucesso! Valor total: R$ {aluguel.valor_total:.2f}")
                return redirect(reverse_lazy('carros:aluguel_success'))
        else:
            messages.error(request, "Erro no formulário. Verifique as datas e tente novamente.")
            return render(request, 'carros/carro_detail.html', {'carro': carro, 'form': form})

    return redirect(reverse('carros:carro_detail', kwargs={'pk': carro.pk}))


def aluguel_success_view(request):
    """
    Página de confirmação após um aluguel bem-sucedido.
    """
    return render(request, 'carros/aluguel_success.html')


# FUNÇÕES AUXILIARES 

def frota(request):
    """
    View de função para listar a frota de carros disponíveis.
    """
    try:
        carros = Carro.objects.filter(disponivel=True).order_by('marca', 'modelo')
        context = {
            'carros': carros
        }
        return render(request, 'frota.html', context)
    except Exception as e:
        print(f"Erro ao carregar frota: {e}")
        messages.error(request, "Erro ao tentar carregar a frota de carros.")
        return redirect(reverse_lazy('carros:home_cliente'))

home_dispatch_view = home_dispatch_view