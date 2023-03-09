
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from jsignature.utils import draw_signature
from notifications.models import Notification
from notifications.signals import notify

from orion import utils
from orion.forms import (CargaHorariaForm, EmpresaForm, EnderecoForm,
                         EquipamentosForm, OrdemServicoForm, SignatureForm)
from orion.models import (CargaHoraria, Empresa, Endereco, Equipamento,
                          Ordem_Servico, SignatureModel)
from usuarios.models import Usuario

from .notifications import (get_notificacoes_nao_lidas,
                            get_numero_notificacoes_nao_lidas)


@login_required
def lista_home(request):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')

    usuario = get_object_or_404(Usuario, user_id=request.user.id)
    #---------------------------
    notificacoes_nao_lidas = get_notificacoes_nao_lidas(request.user)
    numero_notificacoes_nao_lidas = get_numero_notificacoes_nao_lidas(request.user)
    #----------------------------
    ordens_servico = Ordem_Servico.objects.filter(
        aberto_por=usuario, status_chamado='A').order_by('-id')
    contexto = {
        'numero_notificacoes_nao_lidas':numero_notificacoes_nao_lidas,
        'notificacoes_nao_lidas': notificacoes_nao_lidas,
        'ordens_servico': ordens_servico,
        'lista': range(0,10),
        'home': 'Olá, Usuário'
    }
    return render(request, 'orion/pages/chamado.html', contexto)

@login_required
def lista_chamados(request):
    if request.method == "GET":
        ordens_servico = Ordem_Servico.objects.all().filter(
            status_chamado='A').order_by('-id')
        contexto = {
            'ordens_servico': ordens_servico,
            'titulo': 'Chamados abertos'
        }
        return render(request, 'orion/pages/chamado.html', contexto)

@login_required
def busca_chamados(request):
    termo_pesquisado = request.GET.get('q', '').strip()
    
    if not termo_pesquisado:
        raise Http404()
    
    
    ordens_servico = Ordem_Servico.objects.filter( 
                        Q(numero_chamado__icontains = termo_pesquisado) |
                        Q(empresa__nome__icontains = termo_pesquisado) |
                        Q(equipamento__equipamento__icontains = termo_pesquisado)|
                        Q(criado_em__icontains = utils.converter_data(termo_pesquisado)),
                        status_chamado='A'
                        ).order_by('-id')
    contexto = {
        'termo_pesquisado': termo_pesquisado,
        'ordens_servico': ordens_servico,
        'titulo': f'Pesquisa por {termo_pesquisado}...'
    }
    return render(request, 'orion/pages/busca.html', contexto)


@login_required
def novo_chamado_view(request, id):

    #buscando dados salvos sessão 
    OrdemServico_form_data = request.session.get('OrdemServico_form_data', None)
    
    #usando dados de formulario salvos na sessão quando disponiveis
    ordemServicoForm = OrdemServicoForm(OrdemServico_form_data)

    form_carga_horaria_factory = inlineformset_factory(
        Ordem_Servico, CargaHoraria, form=CargaHorariaForm, extra=0 )

    formCargaHoraria = form_carga_horaria_factory()

    contexto = {
        'ordemForm': ordemServicoForm,
        'form_ch': formCargaHoraria, #teste
    }
        
    return render(request, 'orion/pages/novo_chamado.html', contexto)
    

@login_required
def novo_chamado(request):
    if not request.POST:
        raise Http404()

    #salvando a requicao post na sessão 
    request.session['OrdemServico_form_data'] = request.POST
    
    usuario_logado = get_object_or_404(Usuario, user_id=request.user.id)

    ordemForm = OrdemServicoForm(request.POST)
    form_carga_horaria_factory = inlineformset_factory(
        Ordem_Servico, CargaHoraria, form=CargaHorariaForm)

    if ordemForm.is_valid():
        ordem_servico = ordemForm.save(commit=False)
        ordem_servico.aberto_por = usuario_logado
        
        #verificando se numero de chamado gerado já existe.
        if Ordem_Servico.objects.filter(numero_chamado=ordem_servico.numero_chamado).exists():
            messages.error(request, f'chamado {ordem_servico.numero_chamado} já foi cadastrado.' )
            request.session['OrdemServico_form_data'] = None
            return redirect('orion:lista_chamados')

        ordem_servico.save()
        
        formCargaHoraria = form_carga_horaria_factory(request.POST, instance=ordem_servico)
        if formCargaHoraria.is_valid():
            print(formCargaHoraria)
            #formCargaHoraria.instance = ordem_servico
            formCargaHoraria.save()
            messages.success(request, f'chamado {ordem_servico.numero_chamado} criado com sucesso.')
            
        request.session['OrdemServico_form_data'] = None
        return redirect('orion:lista_chamados')

    print(ordemForm)
    return redirect('orion:novo_chamado_view', 0)    

@login_required
def editar_chamado(request, id):
    if request.method == 'GET':
    
        if id != 0:
            print("editar_chamado")
            ordem_servico = get_object_or_404(Ordem_Servico, pk=id)
            
            ordemServicoForm = OrdemServicoForm(instance=ordem_servico) 

            form_carga_horaria_factory = inlineformset_factory(
                Ordem_Servico, CargaHoraria, form=CargaHorariaForm, extra=0)

            formCargaHoraria = form_carga_horaria_factory(instance=ordem_servico)
            
            #carregando todos os horarios relacionados com a instancia de ordem_servico
            lista_carga_horaria = CargaHoraria.objects.select_related('ordem_servico').filter(ordem_servico=id)
            #print("form_ch" ,form_ch)
            ids = ['deletar-elemento-lista-'+str(x) for x in range(0,lista_carga_horaria.count())]
            values = [x for x in range(0,lista_carga_horaria.count())]
            contexto = {
                'ordemForm': ordemServicoForm,
                'form_ch' : formCargaHoraria,
                'carga_horaria' : zip(lista_carga_horaria,ids,values, formCargaHoraria),
                'id' : id,
            }
        
        return render(request, 'orion/pages/editar_chamado.html', contexto)
    else:
        request.session['OrdemServico_form_data'] = request.POST
        ordem_servico = get_object_or_404(Ordem_Servico, pk=id)
        ordemForm = OrdemServicoForm(request.POST, instance=ordem_servico)
        
        form_carga_horaria_factory = inlineformset_factory(
            Ordem_Servico, CargaHoraria, form=CargaHorariaForm)
        
        formCargaHoraria = form_carga_horaria_factory(request.POST, instance=ordem_servico)

        if ordemForm.is_valid() and formCargaHoraria.is_valid():
            chamado = ordemForm.save()
            formCargaHoraria.save()
            #-----------------------------------
            if request.user != chamado.aberto_por.user:
               hoje = datetime.now().strftime("%d/%m/%Y")
               notify.send(request.user, recipient=chamado.aberto_por.user, verb=f"O chamado que você abriu {chamado.numero_chamado}, foi editado por {request.user.username} em {hoje}" )
            #-----------------------------------
            request.session['OrdemServico_form_data'] = None
            return redirect('orion:lista_chamados')
        
        #carregando todos os horarios relacionados com a instancia de ordem_servico
        lista_carga_horaria = CargaHoraria.objects.select_related('ordem_servico').filter(ordem_servico=id)
        #print("form_ch" ,form_ch)
        ids = ['deletar-elemento-lista-'+str(x) for x in range(0,lista_carga_horaria.count())]
        values = [x for x in range(0,lista_carga_horaria.count())]

        messages.error(request, 'Informações nâo válidas')
        return render(request, 'orion/pages/editar_chamado.html', 
        {   'ordemForm': ordemForm,
            'form_ch' : formCargaHoraria,
            'carga_horaria' : zip(lista_carga_horaria,ids,values,formCargaHoraria),
            'id' : id,
        })

@login_required
def deletar_chamado(request, id):
    if request.method == 'POST':
        chamado = get_object_or_404(Ordem_Servico, pk=id)
        print('deletar = ', chamado)
        chamado.delete()
        messages.success(request, f"Chamado deletado com sucesso")
        return redirect('orion:lista_chamados')


@login_required
def chamados_fechados(request):
    ordens_servico = Ordem_Servico.objects.all().filter(
        status_chamado='F').order_by('-id')
    print(ordens_servico)
    contexto = {
        'ordens_servico': ordens_servico,
        'titulo': 'Chamados fechados'
    }
    return render(request, 'orion/pages/chamado.html', contexto)


@login_required
def fechar_chamado(request, id):
    if request.method == 'POST':
        try:
            ordem_servico = get_object_or_404(Ordem_Servico, pk=id)
        except Ordem_Servico.DoesNotExist:
            raise Http404("No Model matches the given query.")
        
        ordem_servico.status_chamado = 'F'
        ordem_servico.save()
        messages.success(request, f"chamado {ordem_servico.numero_chamado} fechado com sucesso")
        return redirect('orion:lista_chamados')


@login_required
def equipamentos(request):

    equipamentos = Equipamento.objects.all().order_by('-id')
    contexto = {
        'equipamentos': equipamentos,
    }
    return render(request, 'orion/pages/equipamentos.html', contexto)



@login_required
def detalhar_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, pk=id)
    print(equipamento)
    if request.method == 'GET':

        equipamentoForm = EquipamentosForm(instance=equipamento)

        contexto = {
            'form': equipamentoForm,
            'id': id
        }

        return render(request, 'orion/pages/detalhes_equipamentos.html', contexto)

    else:
        form = EquipamentosForm(request.POST, instance=equipamento)
        print(form)
        if form.is_valid():
            form.save()

        return redirect('orion:lista_home')


@login_required
def cadastrar_equipamentos(request):
    if request.method == 'GET':
        form = EquipamentosForm()
        contexto = {
            'form': form
        }
        return render(request, 'orion/pages/detalhes_equipamentos.html', contexto)
    else:
        form = EquipamentosForm(request.POST)
        form.save()
        messages.success(request, 'Novo equipamento cadastrado com sucesso')

        return redirect('equipamentos')


def equipamentos_select2(request, id):
    dados = Equipamento.objects.filter(empresa=id)
    dados_json = [{'id': d.id, 'nome': d.equipamento} for d in dados]
    return JsonResponse(dados_json, safe=False)

@login_required
def deletar_equipamento(request, id):
    if request.method == 'POST':
        equipamento = get_object_or_404(Equipamento, pk=id)
        print('deletar = ', equipamento)
        equipamento.delete()
        return redirect('equipamentos')


@login_required
def clientes(request):

    clientes = Empresa.objects.all().order_by('-id')
    contexto = {
        'clientes': clientes,
        'titulo': 'Clientes'
    }
    return render(request, 'orion/pages/clientes.html', contexto)


@login_required
def cadastrar_clientes(request):
    
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        enderecoForm = EnderecoForm(request.POST)
        
        if form.is_valid():
            empresa = form.save(commit=False)
            if enderecoForm.is_valid():
                endereco = enderecoForm.save()
                empresa.endereco = endereco
                messages.error(request, "Endereço informando não válido.")
            
            empresa.save()
            messages.success(request, "Novo Cliente cadastrado com sucesso.")
            return redirect('orion:clientes')
        else:
            if not enderecoForm.is_valid(): 
                enderecoForm.instance = False
            contexto = {
                'form': form,
                'formEndereco': enderecoForm,
                'titulo':'Novo Cliente'
            }
            return render(request, 'orion/pages/detalhes_cliente.html', contexto)

    else:
        form = EmpresaForm()
        formEndereco = EnderecoForm()
        formEndereco.instance = False
        contexto = {
            'form': form,
            'formEndereco': formEndereco,
            'titulo':'Novo Cliente'
            
        }
        return render(request, 'orion/pages/detalhes_cliente.html', contexto)
    

@login_required
def detalhar_cliente(request, id):
    cliente = get_object_or_404(Empresa, pk=id)
    if request.method =='POST':
        form = EmpresaForm(request.POST, instance=cliente)
        enderecoForm = EnderecoForm(request.POST )
        if form.is_valid() and enderecoForm.is_valid() :
            empresa = form.save(commit=False)
            endereco = enderecoForm.save()
            empresa.endereco = endereco
            empresa.save()
        elif form.is_valid():
            form.save()
            messages.success(request, "Cliente salvo com sucesso.")
            if enderecoForm.is_bound:
                messages.error(request, "Endereço informando não válido.")
            
        return redirect('orion:clientes')
    
    else:

        clienteForm = EmpresaForm(instance=cliente)
        enderecoForm = EnderecoForm(instance=cliente.endereco or None) 
        
        if cliente.endereco is None :
            enderecoForm.instance= False

        contexto = {
            'form': clienteForm,
            'formEndereco': enderecoForm,
            'id': id,
            'titulo':'Detalhes Cliente'
        }
        return render(request, 'orion/pages/detalhes_cliente.html', contexto)

@login_required
def deletar_cliente(request):
    if request.method =='POST':
        id = request.POST['id']
        cliente = get_object_or_404(Empresa, pk=id)
        nome = cliente.nome
        if(cliente.endereco):
            endereco = Endereco.objects.filter(pk=cliente.endereco.id).first()
            endereco.delete()
        cliente.delete()
        messages.success(request, f"Cliente {nome} deletado com sucesso")
    return redirect('clientes')

def assinatura_popup(request):

    if request.method == 'GET':
        form = SignatureForm()
        contexto = {
            'form' : form,
        }
        return render(request, 'orion/partials/_assinatura-popup.html', contexto)
            

def marcar_notificacao_como_lida(request):
    if request.POST:
        notificacao_id = request.POST.get('id-notificacao')
        notificacao = Notification.objects.get(id = notificacao_id )
        notificacao.mark_as_read()
        print(notificacao_id, notificacao)
        numero_notificacoes_nao_lidas = get_numero_notificacoes_nao_lidas(request.user)
    return JsonResponse({'count': numero_notificacoes_nao_lidas})



def list_teste(request):

    if request.method == 'GET':
        form = SignatureForm()
        contexto = {
            'form' : form,
        }
        return render(request, 'orion/pages/teste_list.html', contexto)
    else: 
        form = SignatureForm(request.POST or None)
        if form.is_valid():
            form.save()
            signature = form.cleaned_data.get('signature')
            if signature:
                # as an image
                signature_picture = draw_signature(signature)
                # Converta a imagem RGBA em uma imagem RGB
                #signature_picture = signature_picture.convert('RGB')
                signature_picture.save('media/imagem.png', 'PNG')
                return redirect('orion:teste')
            
    


def teste(request):
    if request.method == 'GET':
        obj = SignatureModel.objects.latest('id')
        print("obj " ,obj.signature)
        contexto = {
            'obj' : obj
        }
        return render(request, 'orion/pages/teste.html', contexto)
    
    else: 
        form = SignatureForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('orion:teste')
        


