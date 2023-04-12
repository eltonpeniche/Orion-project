from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from apps.orion import utils
from apps.orion.forms import EquipamentosForm
from apps.orion.models import Equipamento


@login_required
def equipamentos_select2(request, id):
    dados = Equipamento.objects.filter(empresa=id)
    dados_json = [{'id': d.id, 'nome': d.equipamento} for d in dados]
    return JsonResponse(dados_json, safe=False)

@method_decorator(login_required(login_url='usuarios:login' ,redirect_field_name='next'), name='dispatch' )
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

@method_decorator(login_required(login_url='usuarios:login' ,redirect_field_name='next'), name='dispatch' )
class EquipamentoDetail(View):
    
    def get_equipamento(self, id):
        equipamento = None
        if id:  
            equipamento = get_object_or_404(Equipamento, pk=id )

        return equipamento
         

    def render_equipamento(self, form, id ):
        return render(self.request, 'orion/pages/detalhes_equipamentos.html', { 'form': form, 'id': id})

    def get(self, request, id=None):
        equipamento = self.get_equipamento(id)
        equipamentoForm = EquipamentosForm(instance=equipamento)
        return self.render_equipamento(equipamentoForm, id)

    def post(self, request, id=None):
        equipamento = self.get_equipamento(id)
        equipamentoForm = EquipamentosForm(self.request.POST, instance=equipamento)
        
        if equipamentoForm.is_valid():
            messages.success(self.request, "Equipamento Salvo com Sucesso")
            equipamentoForm.save()
            return redirect('orion:equipamentos')
        else:
            return self.render_equipamento(equipamentoForm, id)
            
@method_decorator(login_required(login_url='usuarios:login' ,redirect_field_name='next'), name='dispatch' )
class EquipamentoDelete(EquipamentoDetail):
    def post(self, request, id=None):
        #post(self, *args, **kwargs): self.request.POST.get('id')
        equipamento = self.get_equipamento(id)
        equipamento.delete()
        messages.success(self.request, "Equipamento deletado com sucesso")
        return redirect('orion:equipamentos')