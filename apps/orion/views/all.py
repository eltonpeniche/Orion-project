
import os
from datetime import datetime, time
from time import sleep

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from jsignature.utils import draw_signature
from notifications.models import Notification
from notifications.signals import notify

from apps.orion import utils
from apps.orion.forms import (CargaHorariaForm, DespesaForm, EmpresaForm,
                              EnderecoForm, OrdemServicoForm, SignatureForm,
                              form_model_factory)
from apps.orion.models import CargaHoraria, Chamado, Despesa, Empresa, Endereco
from apps.orion.notifications import (get_notificacoes_nao_lidas,
                                      get_numero_notificacoes_nao_lidas)
from apps.usuarios.models import Usuario

PER_PAGE = os.environ.get('PER_PAGE', 10)



@login_required(login_url="usuarios:login", redirect_field_name="next")
def busca_chamados(request):
    termo_pesquisado = request.GET.get('q', '').strip()
    if not termo_pesquisado:
        messages.error(request, "O campo de busca não pode estar vazio.")
        return redirect(request.META.get('HTTP_REFERER'))
    
    
    chamados = Chamado.objects.select_related('empresa', 'equipamento').filter( 
                        Q(numero_chamado__icontains = termo_pesquisado) |
                        Q(empresa__nome__icontains = termo_pesquisado) |
                        Q(equipamento__equipamento__icontains = termo_pesquisado)|
                        Q(descricao_chamado__icontains = termo_pesquisado)|
                        Q(criado_em__icontains = utils.converter_data(termo_pesquisado)),
                        status_chamado='A'
                        ).order_by('-id')
    
    empresas = Empresa.objects.filter( 
                    Q(nome__icontains = termo_pesquisado) |
                    Q(cnpj__icontains = termo_pesquisado) |
                    Q(telefone__icontains = termo_pesquisado)|
                    Q(email__icontains = termo_pesquisado)
                    ).order_by('-id')
    
    chamados_page =  utils.paginacao(request, chamados)

    empresas_page = utils.paginacao(request, empresas) 

    contexto = {
        'termo_pesquisado': termo_pesquisado,
        'chamados': chamados_page,
        'titulo': f'Pesquisa por "{termo_pesquisado}" em chamados...',
        'titulo_clientes' : f'Pesquisa por "{termo_pesquisado}" em clientes...',
        'empresas': empresas_page
    }
    return render(request, 'orion/pages/busca.html', contexto)


def editar_carga_horaria(request, id):
    if request.method == 'GET':
        ch_obj = get_object_or_404(CargaHoraria, pk = id)
        form_ch = CargaHorariaForm(instance = ch_obj)
        contexto = {
            'form_ch': form_ch,
            'link': reverse('orion:editar_carga_horaria', kwargs={'id': id}),
        } 
        return render(request, 'orion/partials/_carga_horaria_form.html', contexto)
    
    if request.method == 'DELETE':
        ch_obj = get_object_or_404(CargaHoraria, pk = id)
        ch_obj.delete()
        return HttpResponse('')
    
    if request.method == 'POST':

        cargaHoraria = get_object_or_404(CargaHoraria, pk=id)
        form = CargaHorariaForm(request.POST, instance = cargaHoraria)    
        if form.is_valid():
            ch = form.save(commit=False)
            ch.horas_de_trabalho = utils.calcular_horas_trabaho(ch.hora_inicio, ch.hora_termino)
            ch.save()
            template_name = 'orion/partials/_carga_horaria_obj.html'
            return render(request, template_name, {'ch': ch} )
                

        else: 
            return render(request, 'orion/partials/_carga_horaria_form.html', {'form_ch': form})


def nova_carga_horaria(request):
    if request.method == 'POST': 
        id = request.POST.get('id')
        
        if id != None:
            chamado = get_object_or_404(Chamado, pk = id)
            form = CargaHorariaForm(request.POST)    
            request.user.id
            if form.is_valid():
                ch = form.save(commit=False)
                ch.ordem_servico = chamado
                ch.tecnico = request.user
                ch.horas_de_trabalho = utils.calcular_horas_trabaho(ch.hora_inicio, ch.hora_termino)
                ch.save()
                
                template_name = 'orion/partials/_carga_horaria_obj.html'
                return render(request,template_name, {'ch': ch} )
                    

            else: 
                return render(request, 'orion/partials/_carga_horaria_form.html', {'form_ch': form})

        else:
            return HttpResponse('<tr><td colspan="8">Deve Salvar o chamado primeiro</td></tr>')
    
    
    if request.method == 'DELETE':
        return HttpResponse('')
    
    else:
        id = request.GET.get('id')
        formCargaHoraria = CargaHorariaForm()

        contexto = {
            'form_ch': formCargaHoraria,
            'id' : id
        }
        
        return render(request, 'orion/partials/_carga_horaria_form.html', contexto)
  



@login_required(login_url="usuarios:login", redirect_field_name="next")
def novo_chamado(request):
    if request.method == 'POST':
        template_name = 'orion/partials/_detalhes_chamado.html'
        usuario_logado = get_object_or_404(Usuario, user_id=request.user.id)

        ordemForm = OrdemServicoForm(request.POST)
        ordem_servico = None

        if ordemForm.is_valid():
            ordem_servico = ordemForm.save(commit=False)
            ordem_servico.aberto_por = usuario_logado
            
            #verificando se numero de chamado gerado já existe.
            if Chamado.objects.filter(numero_chamado=ordem_servico.numero_chamado).exists():
                
                chamado = Chamado.objects.filter(numero_chamado = ordem_servico.numero_chamado).first()

                ordemForm = OrdemServicoForm(request.POST, instance = chamado)
                ordemForm.save()

                #-----------------------------------
                if request.user != chamado.aberto_por.user:
                    hoje = datetime.now().strftime("%d/%m/%Y")
                    notify.send(request.user, recipient=chamado.aberto_por.user, 
                            verb=f"O chamado que você abriu {chamado.numero_chamado}, foi editado por {request.user.username} em {hoje}" ,
                            target = chamado)
                #-----------------------------------

                cargaHoraria = CargaHoraria.objects.filter(ordem_servico_id = chamado.id)
                
                messages.success(request, f'chamado {ordem_servico.numero_chamado} editado com sucesso.' )
                print('chamado', chamado)
                contexto =  {   'ordemForm': ordemForm, 
                                'id' : chamado.id,  
                                'cargaHoraria' : cargaHoraria}

                return render(request, template_name, contexto )
                
            ordem_servico.save()
            
        else:
            messages.error(request, "Informações não válidas")
            contexto = { 'ordemForm': ordemForm, 'id' : None }
            return render(request, template_name, contexto )

        messages.success(request, "Chamado salvo com sucesso")
        contexto =  {   'ordemForm': ordemForm, 
                        'id' : ordem_servico.id, 
                    }
        return render(request, template_name, contexto)    
    
    else:
        ordemServicoForm = OrdemServicoForm()
        contexto = {
            'ordemForm': ordemServicoForm,
            'id': None
        }
            
        return render(request, 'orion/pages/editar_chamado.html', contexto)
    
        

@login_required(login_url="usuarios:login", redirect_field_name="next")
def editar_chamado(request, id):
    if request.method == 'POST':
        print('\n\npost editar')
        ordem_servico = get_object_or_404(Chamado, pk=id)
        ordemForm = OrdemServicoForm(request.POST, instance=ordem_servico)
    
        if ordemForm.is_valid():
            chamado = ordemForm.save()
            
            #-----------------------------------
            if request.user != chamado.aberto_por.user:
               hoje = datetime.now().strftime("%d/%m/%Y")
               notify.send(request.user, recipient=chamado.aberto_por.user, 
                           verb=f"O chamado que você abriu {chamado.numero_chamado}, foi editado por {request.user.username} em {hoje}" ,
                           target = chamado)
            #-----------------------------------
            #messages.success(request, "Chamado editado com sucesso")
            link = reverse('orion:editar_chamado', kwargs={'id': id} )
            return HttpResponse(f"<button type='submit' class='btn btn-success me-2' hx-post= {link} hx-trigger='click' hx-include='#form-geral-chamado' hx-target='this'  hx-swap='outerHTML' > Salvar <span class='my-indicator'><i class=' fa-solid fa-spinner fa-spin'></i></span> </button>")
        
        else:
            messages.error(request, 'Informações nâo válidas')
            return render(request, 'orion/partials/_detalhes_chamado.html', contexto ) 
        

    
    else:
        print('\n\get editar')
        if id != 0:
            ordem_servico = get_object_or_404(Chamado, pk=id)
            ordemServicoForm = OrdemServicoForm(instance=ordem_servico) 

            cargaHoraria = CargaHoraria.objects.filter(ordem_servico_id = id)


            contexto = {
                'ordemForm': ordemServicoForm,
                'cargaHoraria' : cargaHoraria,
                #'despesa': despesa,
                'id' : id,
            }
        
        return render(request, 'orion/pages/editar_chamado.html', contexto)


@login_required
def deletar_chamado(request, id):
    if request.method == 'POST':
        chamado = get_object_or_404(Chamado, pk=id)
        chamado.delete()
        messages.success(request, f"Chamado deletado com sucesso")
        return redirect('orion:lista_chamados')


@login_required(login_url="usuarios:login", redirect_field_name="next")
def fechar_chamado(request, id):
    if request.method == 'POST':
        try:
            ordem_servico = get_object_or_404(Chamado, pk=id)
        except Chamado.DoesNotExist:
            raise Http404("No Model matches the given query.")
        
        ordem_servico.status_chamado = 'F'
        ordem_servico.save()
        messages.success(request, f"chamado {ordem_servico.numero_chamado} fechado com sucesso")
        return redirect('orion:lista_chamados')



@login_required(login_url="usuarios:login", redirect_field_name="next")
def empresas(request):

    empresas = Empresa.objects.select_related('endereco').all().order_by('-id')
    empresas_page = utils.paginacao(request, empresas)
    contexto = {
        'empresas': empresas_page,
        'titulo': 'Empresas'
    }
    return render(request, 'orion/pages/empresas_list.html', contexto)


@login_required(login_url="usuarios:login", redirect_field_name="next")
def cadastrar_empresa(request):
    
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        enderecoForm = EnderecoForm(request.POST)

        if form.is_valid():
            empresa = form.save(commit=False)
            if enderecoForm.is_valid():
                endereco = enderecoForm.save()
                empresa.endereco = endereco
            else:
                if not enderecoForm.instance: 
                    messages.error(request, "Endereço informando não válido.")
            
            empresa.save()
            messages.success(request, "Novo empresa cadastrada com sucesso.")
            return redirect('orion:empresas')
        else:
            if not enderecoForm.is_valid(): 
                enderecoForm.instance = False
            contexto = {
                'form': form,
                'formEndereco': enderecoForm,
                'titulo':'Nova Empresa'
            }
            return render(request, 'orion/pages/detalhes_empresa.html', contexto)

    else:
        form = EmpresaForm()
        formEndereco = EnderecoForm()
        formEndereco.instance = False
        contexto = {
            'form': form,
            'formEndereco': formEndereco,
            'titulo':'Nova Empresa'
            
        }
        return render(request, 'orion/pages/detalhes_empresa.html', contexto)
    

@login_required(login_url="usuarios:login", redirect_field_name="next")
def detalhar_empresa(request, id):
    empresa = get_object_or_404(Empresa, pk=id)
    if request.method =='POST':
        form = EmpresaForm(request.POST, instance=empresa)
        enderecoForm = EnderecoForm(request.POST )
        if form.is_valid() and enderecoForm.is_valid():
            empresa = form.save(commit=False)
            endereco = enderecoForm.save()
            empresa.endereco = endereco
            empresa.save()
        elif form.is_valid():
            form.save()
            messages.success(request, "Empresa salva com sucesso.")
            if enderecoForm.is_bound:
                messages.error(request, "Endereço informando não válido.")
            
        return redirect('orion:empresas')
    
    else:

        empresaForm = EmpresaForm(instance=empresa)
        enderecoForm = EnderecoForm(instance=empresa.endereco or None) 
        
        if empresa.endereco is None :
            enderecoForm.instance= False

        contexto = {
            'form': empresaForm,
            'formEndereco': enderecoForm,
            'id': id,
            'titulo':'Detalhes Empresa'
        }
        return render(request, 'orion/pages/detalhes_empresa.html', contexto)

@login_required
def deletar_empresa(request):
    if request.method =='POST':
        id = request.POST['id']
        empresa = get_object_or_404(Empresa, pk=id)
        nome = empresa.nome
        if(empresa.endereco):
            endereco = Endereco.objects.filter(pk=empresa.endereco.id).first()
            endereco.delete()
        empresa.delete()
        messages.success(request, f"Empresa {nome} deletado com sucesso")
    return redirect('orion:empresas')

@login_required
def assinatura_popup(request):

    if request.method == 'GET':
        form = SignatureForm()
        contexto = {
            'form' : form,
        }
        return render(request, 'orion/partials/_assinatura-popup.html', contexto)
            

@login_required
def marcar_notificacao_como_lida(request):
    if request.POST:
        notificacao_id = request.POST.get('id-notificacao')
        if Notification.objects.filter(id=notificacao_id).exists():
            notificacao = Notification.objects.get(id = notificacao_id )
            notificacao.mark_as_read()
        notificacoes = get_notificacoes_nao_lidas(request.user) 
        notificacoes_json = serializers.serialize('json', notificacoes )
        numero_notificacoes_nao_lidas = get_numero_notificacoes_nao_lidas(request.user)
    return JsonResponse({'count': numero_notificacoes_nao_lidas, 'notificacoes': notificacoes_json})

@login_required
def download_file(request):
    file_path = 'media/ponto.pdf'
    with open(file_path, 'rb') as f:
        file_content = f.read()
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="meu_ponto.pdf"'
    return response

@login_required
def relatorio_ponto(request):
    usuario = Usuario.objects.select_related('user').filter(user_id = request.user.id)
    
    if request.method == 'GET':
        print(usuario)
        if usuario.first().tipo == 'A':
            usuarioslist = Usuario.objects.select_related('user').all()
        else:
            usuarioslist = usuario
        
        contexto = {
            'title': 'Relatório de Ponto',
            'usuarios': usuarioslist,
        }

        return render(request, "orion/pages/relatorio_ponto.html", contexto)
    if request.method =="POST":
        funcionario_id = request.POST['funcionario']
        funcionario = get_object_or_404(Usuario,id = funcionario_id)
        mes_referencia = request.POST['mes_referencia']
        utils.gerar_relatorio(funcionario, mes_referencia)
        return redirect('orion:download_file')




        
def list_teste(request):
    if request.method == 'GET':
        print('fez get')

        nome = 'name do get'
        email = 'emaildo get '
        contexto = {
            'nome':nome,
            'email':email
        }
        return render(request, 'orion/pages/teste_list.html', contexto)


def teste(request):
    if request.method == 'GET':
        return render(request, 'orion/pages/teste.html')
    
    else: 
        nome = request.POST.get('name')    
        email = request.POST.get('email')    
        
        print(nome, email)

  
        return redirect('orion:teste')
        


