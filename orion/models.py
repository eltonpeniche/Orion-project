
from datetime import datetime, time

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from jsignature.fields import JSignatureField

from usuarios.models import Usuario

#from smart_selects.db_fields import ChainedForeignKey


# from validate_docbr import CPF

# Create your models here.


class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    uf = models.CharField(max_length=2)
    cidade = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro}, {self.cidade}-{self.uf}, {self.cep}'


class Empresa (models.Model):
    nome       = models.CharField(max_length=100)
    cnpj       = models.CharField(max_length=14)
    telefone   = models.CharField(max_length=14, null=True, blank=True)
    email      = models.CharField(max_length=35,null=True, blank=True)
    observacao = models.CharField(max_length=280, null=True, blank=True)#
    endereco   = models.OneToOneField(Endereco, on_delete=models.SET_NULL, 
                                      null=True, blank=True, related_name='empresa')

    
    def __str__(self):
        return f'{self.nome}'


class Equipamento(models.Model):
    empresa          = models.ForeignKey(Empresa, on_delete=models.SET_NULL, related_name='equipamento', null=True, blank=True)
    numero_serie     = models.CharField(max_length=100)
    equipamento      = models.CharField(max_length=100)
    tipo_equipamento = models.CharField(max_length=35)
    descricao        = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.equipamento}'


class TIPO_STATUS(models.TextChoices):
    PARADO = 'P', _('Parado')
    RESTRITO = 'R', _('Restrito')
    NORMAL = 'N', _('Normal')
    OUTROS = 'O', _('Outros')


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

    numero_chamado = models.CharField(max_length=14)  # YYYY DD MM HHHH SS
    descricao_chamado = models.CharField(max_length=150, blank=False)
    descricao_servico = models.TextField(null=True, blank=True)
    # horas_atendimento
    # despesas
    observacoes_do_cliente = models.TextField(blank=True, null = True)
    
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    empresa = models.ForeignKey(
        Empresa, on_delete=models.SET_NULL, related_name='ordem_servico', null=True, blank=True)

    equipamento = models.ForeignKey(Equipamento, on_delete=models.SET_NULL, null=True, blank=True)

    contato = models.CharField(max_length=100, null=True, blank=True)
    
    aberto_por = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, related_name='ordem_servico')

    assinatura = JSignatureField(null=True, blank=True)
    
    def __str__(self):
        return f'Status = {self.status}, Tipo de chamado - {self.tipo_chamado}, - Criado em {self.criado_em}'


class CargaHoraria(models.Model):
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    horas_de_trabalho = models.TimeField()
    status = models.CharField(
        max_length=1, choices=TIPO_STATUS.choices, blank=False, null=False, default='N')
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='carga_horaria')

    ordem_servico = models.ForeignKey(
        Ordem_Servico, on_delete=models.SET_NULL, null=True, related_name='carga_horaria')

    def __str__(self):
        return f'dia = {self.data} -Entrada =  {self.hora_inicio} -Saida =  {self.hora_termino}'

    def save(self, *args, **kwargs):
        # Convertendo cada objeto datetime.time em um objeto datetime
        hora_inicio = datetime.combine(self.data, self.hora_inicio)
        hora_termino = datetime.combine(self.data, self.hora_termino)
        
        # Calcule a diferença entre os dois horarios
        diferenca = hora_termino - hora_inicio
        
        diferenca_horas, diferenca_segundos = divmod(diferenca.seconds, 3600)
        diferenca_minutos, _ = divmod(diferenca_segundos, 60)
        #horas trabalhadas
        self.horas_de_trabalho= time(hour=diferenca_horas, minute=diferenca_minutos, second=0)
        super(CargaHoraria, self).save(*args, **kwargs)


class TIPO_DESPESA(models.TextChoices):
    ALIMENTACAO = 'AL', _('Alimentação')
    BAGAGEM = 'BA', _('Bagagem')
    ALUGUEL_CARROS = 'AC', _('Aluguel de carros')
    COMBUSTIVEL = 'CO', _('Combustível')
    CORREIO_FRETE = 'CF', _('Correio/Frete')
    ESTACIONAMENTO = 'ES', _('Estacionamento')
    FRIGOBAR = 'FR', _('Friogobar')
    HOSPEDAGEM = 'HO', _('Hospedagem')
    LAVANDERIA = 'LA', _('Lavanderia')
    COMPRA_DE_MATERIAL = 'CM', _('Compra de material')
    PAGAMENTOS = 'PG', _('Pagamentos')
    PASSAGEM_AERIA = 'PA', _('Passagem Aéria')
    TRANSPORTE = 'TR', _('Transporte')
    OUTROS = 'OT', _('Outros')

class Despesa(models.Model):
    tipo = models.CharField(
        max_length=2, choices=TIPO_DESPESA.choices, blank=False, null=False, default='AL')
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='despesa')
    ordem_servico = models.ForeignKey(Ordem_Servico, on_delete=models.SET_NULL, null=True, related_name='despesa')

    def __str__(self):
        return f'tipo = {self.tipo} -data =  {self.data} - valor =  {self.valor}'


class SignatureModel(models.Model):
    signature = JSignatureField()