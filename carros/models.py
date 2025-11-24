from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 
from datetime import date, timedelta 

# 1. MODELOS DE PERFIL
class Cliente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cliente')
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    cnh = models.CharField(max_length=20, unique=True, verbose_name="CNH")
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# Perfil do Colaborador
class Colaborador(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='colaborador')
    matricula = models.CharField(max_length=10, unique=True, verbose_name="Matrícula")

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        
    def __str__(self):
        return self.user.get_full_name() or self.user.username

# 2. MODELO CARRO
class Carro(models.Model):
    placa = models.CharField(max_length=10, unique=True, verbose_name="Placa")
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    ano = models.PositiveIntegerField(verbose_name="Ano")
    valor_diaria = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valor da Diária")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível para Aluguel")

    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"


# 3. MODELO ALUGUEL 
class Aluguel(models.Model):
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='alugueis'
    )
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField() 
    data_devolucao = models.DateField(null=True, blank=True, verbose_name="Data Real de Devolução")

    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = "Aluguel"
        verbose_name_plural = "Aluguéis"

    def __str__(self):
        status = "(Concluído)" if self.data_devolucao else "(Ativo)"
        return f"Aluguel de {self.carro.modelo} por {self.cliente.username} {status}"
    
    def save(self, *args, **kwargs):
      
        data_final = self.data_devolucao if self.data_devolucao else self.data_fim
        
        if self.data_inicio and data_final and self.carro_id:
            delta = data_final - self.data_inicio
            dias = delta.days
            dias_calculados = max(1, dias + 1)
            self.valor_total = dias_calculados * self.carro.valor_diaria

        super().save(*args, **kwargs)