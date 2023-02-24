from django.contrib import admin

from orion.models import (CargaHoraria, Empresa, Endereco, Equipamento,
                          Ordem_Servico)

# Register your models here.


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ( 'id','rua', 'numero', 'bairro', 'cep', 'uf', 'cidade')
    list_display_links = ( 'id','rua', 'numero', 'bairro', 'cep', 'uf', 'cidade')
    ordering = ('id',)



@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ( 'id','nome', 'cnpj', 'telefone', 'email', 'observacao')
    list_display_links = ( 'id','nome', 'cnpj', 'telefone', 'email', 'observacao')
    ordering = ('id',)


class CargaHorariaInline(admin.StackedInline):
    model = CargaHoraria
    extra = 0
    # readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']
    # fields = ['name', 'quanity', 'unit', 'directions']


@admin.register(Ordem_Servico)
class Ordem_ServicoAdmin(admin.ModelAdmin):
    inlines = [CargaHorariaInline]
    list_display = ('id', 'numero_chamado', 'descricao_chamado',
                    'get_tipo_chamado_display', 'equipamento', 'criado_em', 'get_status_display', 'get_status_chamado_display')
    list_display_links = ('id', 'numero_chamado', 'descricao_chamado',
                    'get_tipo_chamado_display', 'equipamento', 'criado_em', 'get_status_display', 'get_status_chamado_display')
    ordering = ('id',)

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'numero_serie', 'equipamento', 'tipo_equipamento','empresa', 'descricao')
    list_display_links = ( 'id', 'numero_serie', 'equipamento', 'tipo_equipamento','empresa', 'descricao')
    ordering = ('id',)


@admin.register(CargaHoraria)
class CargaHorariaAdmin(admin.ModelAdmin):
    ... 


