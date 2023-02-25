from datetime import date, datetime, time, timedelta

from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.forms.models import formset_factory, inlineformset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from orion.models import (CargaHoraria, Empresa, Endereco, Equipamento,
                          Ordem_Servico)
from usuarios.models import Usuario

from .forms import (CargaHorariaForm, EmpresaForm, EnderecoForm,
                    EquipamentosForm, OrdemServicoForm)


def lista_home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    usuario = get_object_or_404(Usuario, user_id=request.user.id)
    ordens_servico = Ordem_Servico.objects.filter(
        aberto_por=usuario, status_chamado='A').order_by('-id')
    contexto = {
        'ordens_servico': ordens_servico,
        'home': 'Olá, Usuário'
    }
    return render(request, 'orion/pages/chamado.html', contexto)


def lista_chamados(request):
    if request.method == "GET":
        ordens_servico = Ordem_Servico.objects.all().filter(
            status_chamado='A').order_by('-id')
        contexto = {
            'ordens_servico': ordens_servico,
            'titulo': 'Chamados abertos'
        }
        return render(request, 'orion/pages/chamado.html', contexto)


def novo_chamado_view(request, id):

    #buscando dados salvos sessão 
    OrdemServico_form_data = request.session.get('OrdemServico_form_data', None)
    
    #usando dados de formulario salvos na sessão quando disponiveis
    ordemServicoForm = OrdemServicoForm(OrdemServico_form_data)

    form_carga_horaria_factory = inlineformset_factory(
        Ordem_Servico, CargaHoraria, form=CargaHorariaForm, extra=0)

    formCargaHoraria = form_carga_horaria_factory()

    contexto = {
        'ordemForm': ordemServicoForm,
        'form_ch': formCargaHoraria, #teste
    }
        
    return render(request, 'orion/pages/novo_chamado.html', contexto)
    


def novo_chamado(request):
    if not request.POST:
        raise Http404()

    #salvando a requicao post na sessão 
    request.session['OrdemServico_form_data'] = request.POST
    
    usuario = get_object_or_404(Usuario, user_id=request.user.id)

    ordemForm = OrdemServicoForm(request.POST)
    form_carga_horaria_factory = inlineformset_factory(
        Ordem_Servico, CargaHoraria, form=CargaHorariaForm)

    if ordemForm.is_valid():
        ordem_servico = ordemForm.save(commit=False)
        
        #verificando se numero de chamado gerado já existe.
        if Ordem_Servico.objects.filter(numero_chamado=ordem_servico.numero_chamado).exists():
            messages.error(request, f'chamado {ordem_servico.numero_chamado} já foi cadastrado.' )
            request.session['OrdemServico_form_data'] = None
            return redirect('lista_chamados')

        ordem_servico.aberto_por = usuario
        ordem_servico.save()
        
        formCargaHoraria = form_carga_horaria_factory(request.POST)
        if formCargaHoraria.is_valid():
            print(formCargaHoraria)
            formCargaHoraria.instance = ordem_servico
            formCargaHoraria.save()
            messages.success(request, f'chamado {ordem_servico.numero_chamado} criado com sucesso.')
            
        request.session['OrdemServico_form_data'] = None
        return redirect('lista_chamados')

    return redirect('novo_chamado_view', 0)    

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
            
            contexto = {
                'ordemForm': ordemServicoForm,
                'form_ch' : formCargaHoraria,
                'carga_horaria' : lista_carga_horaria,
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

        if ordemForm.is_valid():
            ordemForm.save()
            
            if formCargaHoraria.is_valid():
                formCargaHoraria.save()
                request.session['OrdemServico_form_data'] = None
                return redirect('lista_chamados')
        print(formCargaHoraria)
        print("não foi valido")
        return redirect('novo_chamado_view', id)  


def deletar_chamado(request, id):

    chamado = get_object_or_404(Ordem_Servico, pk=id)
    print('deletar = ', chamado)
    chamado.delete()
    messages.success(request, f"Chamado deletado com sucesso")
    return redirect('lista_home')


def chamados_fechados(request):
    ordens_servico = Ordem_Servico.objects.all().filter(
        status_chamado='F').order_by('-id')
    print(ordens_servico)
    contexto = {
        'ordens_servico': ordens_servico,
        'titulo': 'Chamados fechados'
    }
    return render(request, 'orion/pages/chamado.html', contexto)

def fechar_chamado(request, id):
    try:
        ordem_servico = get_object_or_404(Ordem_Servico, pk=id)
    except Ordem_Servico.DoesNotExist:
        raise Http404("No Model matches the given query.")
    
    ordem_servico.status_chamado = 'F'
    ordem_servico.save()
    messages.success(request, f"chamado {ordem_servico.numero_chamado} fechado com sucesso")
    return redirect(lista_chamados)

def equipamentos(request):

    equipamentos = Equipamento.objects.all().order_by('-id')
    contexto = {
        'equipamentos': equipamentos,
    }
    return render(request, 'orion/pages/equipamentos.html', contexto)


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

        return redirect('home')


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


def deletar_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, pk=id)
    print('deletar = ', equipamento)
    equipamento.delete()
    return redirect('equipamentos')


def clientes(request):

    clientes = Empresa.objects.all().order_by('-id')
    contexto = {
        'clientes': clientes,
        'titulo': 'Clientes'
    }
    return render(request, 'orion/pages/clientes.html', contexto)


def detalhar_cliente(request, id):
    cliente = get_object_or_404(Empresa, pk=id)
    print(cliente.contato)
    if request.method == 'GET':

        clienteForm = EmpresaForm(instance=cliente)
        formEndereco = EnderecoForm(instance=cliente.endereco)
        formContato = ContatoForm(instance=cliente.contato)

        contexto = {
            'form': clienteForm,
            'formEndereco': formEndereco,
            'formContato': formContato,
            'id': id
        }

        return render(request, 'orion/pages/detalhes_cliente.html', contexto)

    else:
        form = EmpresaForm(request.POST, instance=cliente)
        formEndereco = EnderecoForm(request.POST, instance=cliente.endereco)
        formContato = ContatoForm(request.POST, instance=cliente.contato)
        print(form)
        if form.is_valid():
            form.save()
            formEndereco.save()
            formContato.save()

        return redirect('clientes')


def deletar_cliente(request, id):
    cliente = get_object_or_404(Empresa, pk=id)
    contato = get_object_or_404(Contato, pk=cliente.contato.id)
    endereco = get_object_or_404(Endereco, pk=cliente.endereco.id)
    cliente.delete()
    contato.delete()
    endereco.delete()
    return redirect('clientes')


def cadastrar_clientes(request):
    if request.method == 'GET':
        form = EmpresaForm()
        formEndereco = EnderecoForm()
        
        contexto = {
            'form': form,
            'formEndereco': formEndereco,
            
        }
        return render(request, 'orion/pages/detalhes_cliente.html', contexto)
    else:
        form = EmpresaForm(request.POST)

        formEndereco = EnderecoForm(request.POST)

        endereco = formEndereco.save()
        empresa = form.save(commit=False)
        empresa.endereco = endereco
       
        empresa.save()

        return redirect('clientes')

def list_teste(request):

    ordens_servico = Ordem_Servico.objects.all().order_by('-id')
    contexto = {
        'ordens_servico': ordens_servico,
    }
    return render(request, 'orion/pages/teste_list.html', contexto)


def teste(request):
    if request.method == 'GET':
        form = OrdemServicoForm()
        form_carga_horaria_factory = inlineformset_factory(Ordem_Servico, CargaHoraria, form=CargaHorariaForm, extra=0)
        
        form_ch = form_carga_horaria_factory()
        
        contexto = {
            'form': form,
            'form_ch': form_ch
        }
        return render(request, 'orion/pages/teste.html', contexto)
    else:
        ordemForm = OrdemServicoForm(request.POST)
        
        form_carga_horaria_factory = inlineformset_factory(
            Ordem_Servico, CargaHoraria, form=CargaHorariaForm)
        
        formCargaHoraria = form_carga_horaria_factory(request.POST)

        if ordemForm.is_valid():
            ordem_servico = ordemForm.save()
            
            if formCargaHoraria.is_valid():
                formCargaHoraria.instance = ordem_servico
                formCargaHoraria.save()
                return redirect('lista_chamados')
        print(formCargaHoraria)
        print("não foi valido")
        return redirect('lista_home')  



def teste_create(request):
    if not request.POST:
        raise Http404

    ordemForm = OrdemServicoForm(request.POST)
    form_carga_horaria_factory = inlineformset_factory(
        Ordem_Servico, CargaHoraria, form=CargaHorariaForm)
    
    formCargaHoraria = form_carga_horaria_factory(request.POST)
    
    if ordemForm.is_valid() and formCargaHoraria.is_valid():
        ordem_servico = ordemForm.save()
        formCargaHoraria.instance = ordem_servico
        formCargaHoraria.save()
        return redirect('list_teste')
    
    contexto = {
        'formCargaHoraria': formCargaHoraria,
        'ordemForm': ordemForm
    }
    return render(request, 'orion/pages/teste.html', contexto)

