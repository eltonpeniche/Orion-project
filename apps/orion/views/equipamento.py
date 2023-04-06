from django.views.generic import ListView

from apps.orion import utils
from apps.orion.models import Equipamento
from apps.usuarios.models import Usuario


class EquipamentoList(ListView):
    model = Equipamento
    context_object_name = "equipamentos"
    template_name = 'orion/pages/equipamentos.html'
    ordering = '-id'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.select_related('empresa')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        equipamento_page = utils.paginacao(self.request, ctx.get('equipamentos'))
        ctx.update({'equipamentos': equipamento_page })
        return ctx
    