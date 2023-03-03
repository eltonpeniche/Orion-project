from datetime import date, datetime, time, timedelta

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import formset_factory, inlineformset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from orion.forms import (CargaHorariaForm, EmpresaForm, EnderecoForm,
                         EquipamentosForm, OrdemServicoForm)
from orion.models import (CargaHoraria, Empresa, Endereco, Equipamento,
                          Ordem_Servico)
from usuarios.models import Usuario


@login_required
def lista_home(request):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')

    usuario = get_object_or_404(Usuario, user_id=request.user.id)
    ordens_servico = Ordem_Servico.objects.filter(
        aberto_por=usuario, status_chamado='A').order_by('-id')
    contexto = {
        'ordens_servico': ordens_servico,
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
            ordemForm.save()
            formCargaHoraria.save()
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
            return redirect('clientes')
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
        
        ch = CargaHoraria.objects.fi
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

