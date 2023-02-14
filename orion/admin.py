from django.contrib import admin

from orion.models import (CargaHoraria, Contato, Empresa, Endereco,
                          Equipamento, Ordem_Servico, Usuario)

# Register your models here.


class UsuarioAdmin(admin.ModelAdmin):
    ...


admin.site.register(Usuario, UsuarioAdmin)


class EnderecoAdmin(admin.ModelAdmin):
    ...


admin.site.register(Endereco, EnderecoAdmin)


class ContatoAdmin(admin.ModelAdmin):
    ...


admin.site.register(Contato, ContatoAdmin)


class EmpresaAdmin(admin.ModelAdmin):
    ...


admin.site.register(Empresa, EmpresaAdmin)

class CargaHorariaInline(admin.StackedInline):
    model = CargaHoraria
    extra = 0
    #readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']
    # fields = ['name', 'quanity', 'unit', 'directions']
    
class Ordem_ServicoAdmin(admin.ModelAdmin):
    inlines = [CargaHorariaInline]
    list_display = ('id','numero_chamado', 'descricao_chamado',
                    'get_tipo_chamado_display', 'equipamento', 'criado_em', 'get_status_display', 'get_status_chamado_display')


admin.site.register(Ordem_Servico, Ordem_ServicoAdmin)


class EquipamentoAdmin(admin.ModelAdmin):
    ...


admin.site.register(Equipamento, EquipamentoAdmin)

class CargaHorariaAdmin(admin.ModelAdmin):
    ...

admin.site.register(CargaHoraria, CargaHorariaAdmin)


