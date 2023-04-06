from django.views.generic import ListView

from apps.orion import utils
from apps.orion.models import Chamado
from apps.usuarios.models import Usuario


class ChamadoList(ListView):
    model = Chamado
    context_object_name = "chamados"
    template_name = 'orion/pages/chamado_list.html'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        
        qs = qs.select_related('empresa', 'equipamento').filter(status_chamado='A').order_by('-id')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        chamado_page = utils.paginacao(self.request, ctx.get('chamados'))
        ctx.update({'chamados': chamado_page })
        ctx['titulo'] = f'Chamados abertos'
        return ctx
    

class ChamadoHomeList(ChamadoList):

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        usuario = Usuario.objects.get(user_id=self.request.user.id)
        qs = qs.filter(aberto_por=usuario)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['home'] = f'Olá, {self.request.user.username.title()}'
        return ctx
    

class ChamadosFechadosList(ChamadoList):

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        
        qs = Chamado.objects.all().select_related('empresa', 'equipamento').filter(
        status_chamado='F').order_by('-id')
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['titulo'] = f'Chamados fechados'
        return ctx
