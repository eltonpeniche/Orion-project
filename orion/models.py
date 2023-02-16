
from django.contrib.auth.models import User
from django.db import models
from django.forms.formsets import formset_factory
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey

from django.dispatch import receiver
from django.db.models.signals import post_save
# from validate_docbr import CPF

# Create your models here.


class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    uf = models.CharField(max_length=2)
    cidade = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro}, {self.cidade}-{self.uf}, {self.cep}'


class Contato(models.Model):
    nomeContato = models.CharField(max_length=100)
    telefone = models.CharField(max_length=14)
    email = models.CharField(max_length=35)

    def __str__(self):
        return self.nomeContato


class Empresa (models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)
    telefone = models.CharField(max_length=14)
    email = models.CharField(max_length=35)
    observacao = models.CharField(max_length=280)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome}'


class Equipamento(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True)
    numero_serie = models.CharField(max_length=100)
    equipamento = models.CharField(max_length=100)
    tipo_equipamento = models.CharField(max_length=35)
    descricao = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return f'{self.equipamento}'


class TIPO_STATUS(models.TextChoices):
    PARADO = 'P', _('Parado')
    RESTRITO = 'R', _('Restrito')
    NORMAL = 'N', _('Normal')
    OUTROS = 'O', _('Outros')

class TIPO_USUARIO(models.TextChoices):
    ADMIN = 'A', _('Admin')
    TECNICO = 'T', _('Tecnico')

class Usuario(models.Model):
    user = models.OneToOneField(
        User, related_name='usuarios', on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=1, choices=TIPO_USUARIO.choices)
    
    def __str__(self):
        return f'{self.user.username}'


class Ordem_Servico(models.Model):
    #    STATUS = (('P', 'PARADO'), ('R', 'RESTRITO'),
    #              ('N', 'NORMAL'), ('O', 'OUTROS'))
    TIPO_DE_CHAMADO = (('C', 'Contrato'), ('A', 'Avulso'))
    STATUS_CHAMADO = (('A', 'Aberto'), ('F', 'Fechado'))

    status = models.CharField(
        max_length=1, choices=TIPO_STATUS.choices, blank=False, null=False, default='P')

    tipo_chamado = models.CharField(
        max_length=1, choices=TIPO_DE_CHAMADO, blank=False, null=False, default='C')

    status_chamado = models.CharField(
        max_length=1, choices=STATUS_CHAMADO, default='A')

    numero_chamado = models.CharField(max_length=14 )  # YYYY DD MM HHHH SS
    descricao_chamado = models.CharField(max_length=150, blank=False)
    descricao_servico = models.TextField(blank=True)
    # horas_atendimento
    # despesas
    observacoes_do_cliente = models.TextField(blank=True)
    # assinatura
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, blank=True, null=True)
    
    #equipamento = models.ForeignKey(Equipamento, on_delete=models.SET_NULL, blank=True, null=True)
    equipamento = ChainedForeignKey( Equipamento, chained_field="empresa",
        chained_model_field="empresa", show_all=False, auto_choose=True, sort=True)

    contato = ChainedForeignKey( Contato, chained_field="empresa", chained_model_field="empresa", show_all=False, auto_choose=True, sort=True)

    aberto_por = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f'Status = {self.status}, Tipo de chamado - {self.tipo_chamado}, - Criado em {self.criado_em}'


class CargaHoraria(models.Model):
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    #total_horas 
    status = models.CharField( max_length=1, choices=TIPO_STATUS.choices, blank=False, null=False, default='N')
    #técnico
    ordem_servico = models.ForeignKey(Ordem_Servico, on_delete=models.SET_NULL, null=True, related_name='carga_horaria')

    def __str__(self):
        return f'dia = {self.data} -Entrada =  {self.hora_inicio} -Saida =  {self.hora_termino}'

    


