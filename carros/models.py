from django.db import models

class Carro(models.Model):
    """Representa um carro disponível para aluguel."""
    
    MARCAS = (
        ('VW', 'Volkswagen'),
        ('FIAT', 'Fiat'),
        ('GM', 'General Motors'),
        ('FORD', 'Ford'),
        ('TOYOTA', 'Toyota'),
        ('HYUNDAI', 'Hyundai'),
    )
    
    placa = models.CharField(max_length=8, unique=True, verbose_name="Placa")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    marca = models.CharField(max_length=50, choices=MARCAS, verbose_name="Marca")
    ano = models.IntegerField(verbose_name="Ano de Fabricação")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível para Aluguel")
    valor_diaria = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor Diária (R$)")

    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"
        
    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"

class Cliente(models.Model):
    """Representa um cliente da locadora."""
    nome = models.CharField(max_length=200, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF") # Deve ser formatado na entrada
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome

class Aluguel(models.Model):
    """Representa um aluguel de carro realizado."""
    
    carro = models.ForeignKey(Carro, on_delete=models.PROTECT, limit_choices_to={'disponivel': True}, verbose_name="Carro Alugado")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name="Cliente")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data Prevista de Devolução")
    data_devolucao = models.DateField(null=True, blank=True, verbose_name="Data Real de Devolução")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Total (R$)")

    class Meta:
        verbose_name = "Aluguel"
        verbose_name_plural = "Aluguéis"
        
    def __str__(self):
        return f"Aluguel do {self.carro.modelo} para {self.cliente.nome}"
    
    def save(self, *args, **kwargs):
        if not self.pk and self.carro.disponivel:
            self.carro.disponivel = False
            self.carro.save()
            
        super().save(*args, **kwargs)

from django.contrib import admin
admin.site.register(Carro)
admin.site.register(Cliente)
admin.site.register(Aluguel)
