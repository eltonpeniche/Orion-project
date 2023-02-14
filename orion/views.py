from datetime import date, datetime, time, timedelta

from django.forms.models import formset_factory, inlineformset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from orion.models import (CargaHoraria, Contato, Empresa, Endereco,
                          Equipamento, Ordem_Servico, Usuario)

from .forms import (CargaHorariaForm, ContatoForm, EmpresaForm, EnderecoForm,
                    EquipamentosForm, OrdemServicoForm)

# Create your views here.


def lista_home(request):

    ordens_servico = Ordem_Servico.objects.all().order_by('-id')
    contexto = {
        'ordens_servico': ordens_servico,
        'home' : 'Olá, Usuário'
    }
    return render(request, 'orion/pages/chamado.html', contexto)


def lista_chamados(request):
    if request.method =="GET": 
        ordens_servico = Ordem_Servico.objects.all().filter(
            status_chamado='A').order_by('-id')
        contexto = {
            'ordens_servico': ordens_servico,
            'titulo': 'Chamados abertos'
        }
        return render(request, 'orion/pages/chamado.html', contexto)


def editar_chamado(request, id):
    if request.method == "GET": 

        ordem_servico = get_object_or_404(Ordem_Servico, pk = id)
        ordemServicoForm = OrdemServicoForm(instance=ordem_servico) 

        form_ch = CargaHorariaForm(instance=ordem_servico)
        
        #carregando todos os horarios relacionados com a instancia de ordem_servico
        lista_carga_horaria = CargaHoraria.objects.select_related('ordem_servico').filter(ordem_servico=id)
        #print("form_ch" ,form_ch)
        
        contexto = {
            'ordemForm': ordemServicoForm,
            'form_ch' : form_ch,
            'carga_horaria' : lista_carga_horaria,
            'id' : id,
        }
        
        #return render(request, 'orion/pages/teste.html', contexto)
        return render(request, 'orion/pages/detalhes_chamado.html', contexto)

    else:
        print(request.POST)
        ordem_servico = get_object_or_404(Ordem_Servico, pk = id)
    
        ordemForm = OrdemServicoForm(request.POST, instance=ordem_servico )
        form_ch = CargaHorariaForm(request.POST )
        #carregando todos os horarios relacionados com a instancia de ordem_servico
        lista_carga_horaria = CargaHoraria.objects.select_related('ordem_servico').filter(ordem_servico=id)
        
        if ordemForm.is_valid() and form_ch.is_valid():
            print("é valido")
            ordemForm.save()
            ch = form_ch.save(commit=False)
            ch.ordem_servico = ordem_servico
            ch.save()
            if 'salvar_modal' in request.POST:
                contexto = { 
                    'ordemForm': ordemForm,
                    'form_ch' : form_ch,
                    'carga_horaria' : lista_carga_horaria,
                    'id' : id,
                }
                return render(request, 'orion/pages/detalhes_chamado.html', contexto)
            return redirect("lista_home")
        else:
            contexto = {
                'ordemForm': ordemForm,
                #'carga_horaria' : carga_horaria,
                'form_ch' :form_ch,
                'id' : id,
            }
            return render(request, 'orion/pages/detalhes_chamado.html', contexto)


def novo_chamado(request):
    if request.method == 'GET':
        ordemServicoForm = OrdemServicoForm()
        contexto = {
            'ordemForm': ordemServicoForm,
            'id': 0
        }
        return render(request, 'orion/pages/detalhes_chamado.html', contexto)
    else:
        form = OrdemServicoForm(request.POST) 
        form.save()

        return redirect('home')


def deletar_chamado(request,id):
        chamado = get_object_or_404(Ordem_Servico, pk=id)
        print('deletar = ', chamado)
        chamado.delete()
        return redirect('home')


def chamados_fechados(request):
    ordens_servico = Ordem_Servico.objects.all().filter(status_chamado = 'F' ).order_by('-id')
    print(ordens_servico)
    contexto = {
        'ordens_servico': ordens_servico,
        'titulo' : 'Chamados fechados'
    }
    return render(request, 'orion/pages/chamado.html', contexto)

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
        'id' : id
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
            'form' : form
        }
        return render(request, 'orion/pages/detalhes_equipamentos.html', contexto)
    else:
        form = EquipamentosForm(request.POST) 
        form.save()
        
        return redirect('equipamentos')


def deletar_equipamento(request,id):
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
            'formEndereco' : formEndereco,
            'formContato' : formContato,
            'id' : id
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

def deletar_cliente(request,id):
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
        formContato = ContatoForm()
        contexto = {
            'form' : form,
            'formEndereco' : formEndereco,
            'formContato' : formContato
        }
        return render(request, 'orion/pages/detalhes_cliente.html', contexto)
    else:
        form = EmpresaForm(request.POST) 

        formEndereco = EnderecoForm(request.POST)

        formContato = ContatoForm(request.POST)
        
        endereco = formEndereco.save() 
        contato = formContato.save()
        empresa = form.save(commit=False)
        empresa.endereco = endereco
        empresa.contato = contato
        empresa.save()


        
        return redirect('clientes')

def teste(request):
    teste_create_data = request.session.get('teste_create_data', None)
    ordemServicoForm = OrdemServicoForm()
    form_carga_horaria_factory = inlineformset_factory(Ordem_Servico, CargaHoraria, form = CargaHorariaForm, extra = 1 )

    formCargaHoraria = form_carga_horaria_factory()

    contexto = {
        'form': formCargaHoraria,
        'ordemServicoForm' : ordemServicoForm
    }

    return render(request, 'orion/pages/teste.html', contexto)
   

def teste_create(request):
    if not request.POST:
        raise Http404;

    POST = request.POST
    request.session['teste_create_data'] = POST
    form = CargaHorariaForm(request.POST)
    return redirect('teste')
