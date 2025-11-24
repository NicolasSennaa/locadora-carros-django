from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction 
from django.core.exceptions import ValidationError
from datetime import date
from django.db.models import Q
from .models import Cliente, Aluguel, Carro 

# 1. Formulário de Registro de Cliente

class ClienteRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="Nome")
    last_name = forms.CharField(max_length=150, required=True, label="Sobrenome")
    email = forms.EmailField(required=True, label="E-mail")
    cpf = forms.CharField(max_length=14, required=True, label="CPF")
    cnh = forms.CharField(max_length=20, required=True, label="CNH")
    telefone = forms.CharField(max_length=15, required=False, label="Telefone")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
        
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        
        if commit:
            user.save()
        Cliente.objects.create(
            user=user,
            cpf=self.cleaned_data.get('cpf'),
            cnh=self.cleaned_data.get('cnh'),
            telefone=self.cleaned_data.get('telefone')
        )
        return user

# 2. Formulário de Aluguel

class AluguelForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.carro = kwargs.pop('carro', None) 
        super().__init__(*args, **kwargs)
        self.fields['data_inicio'].widget.attrs.update({
            'class': 'form-input w-full rounded-md border-gray-300 shadow-sm'
        })
        self.fields['data_fim'].widget.attrs.update({
            'class': 'form-input w-full rounded-md border-gray-300 shadow-sm'
        })

    class Meta:
        model = Aluguel
        fields = ['data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        hoje = date.today()

        if not self.carro:
            raise ValidationError("O formulário de aluguel não está associado a um carro.", code='missing_car')

        if data_inicio and data_fim:
            
            if data_inicio < hoje:
                self.add_error('data_inicio', "A data de início não pode ser anterior à data de hoje.")
            
            if data_fim <= data_inicio:
                self.add_error('data_fim', "A data de fim deve ser posterior à data de início.")
            
            if self.errors:
                return cleaned_data

            conflitos = Aluguel.objects.filter(
                carro=self.carro,
                data_devolucao__isnull=True 
            ).exclude(
                data_fim__lt=data_inicio
            ).exclude(
                data_inicio__gt=data_fim
            )
            
            if self.instance.pk:
                conflitos = conflitos.exclude(pk=self.instance.pk)

            if conflitos.exists():
                conflito = conflitos.first()
                self.add_error(
                    None,
                    f"O carro já está alugado ou reservado de {conflito.data_inicio.strftime('%d/%m/%Y')} até {conflito.data_fim.strftime('%d/%m/%Y')}. Escolha outras datas."
                )

        return cleaned_data