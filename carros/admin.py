from django.contrib import admin
from .models import Carro, Aluguel, Cliente, Colaborador

class ClienteInline(admin.StackedInline):
    model = Cliente
    can_delete = False
    verbose_name_plural = 'Perfil de Cliente'

class ColaboradorInline(admin.StackedInline):
    model = Colaborador
    can_delete = False
    verbose_name_plural = 'Perfil de Colaborador'

admin.site.register(Cliente)
admin.site.register(Colaborador)
admin.site.register(Aluguel)

class CarroAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'placa', 'disponivel', 'valor_diaria')
    list_filter = ('disponivel', 'modelo')
    search_fields = ('modelo', 'placa')

admin.site.register(Carro, CarroAdmin)