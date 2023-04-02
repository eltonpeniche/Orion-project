
from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.usuarios.forms import (CadastroUsuarioForm, LoginForm,
                                 UserUpdateForm, UsuarioForm)

from .models import Usuario


#utils
def isUserAdmin(user):
    usuario = get_object_or_404(Usuario, user_id=user.id)
    if usuario.tipo == 'A':
        return True
    return False

@login_required
def lista_usuarios(request):
    usuarios = Usuario.objects.select_related('user').all()
    contexto = {
        'forms': usuarios,
        'titulo': 'Lista de Usuários'
    }
    return render(request, 'usuarios/pages/lista_usuarios.html', contexto)

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "Logout realizado com sucesso")
    print("Logout realizado com sucesso")
    return redirect(reverse('usuarios:login'))


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('orion:lista_home'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form['login'].value().lower().strip()
            senha = form['senha'].value()
            usuario = auth.authenticate(
                request,
                username=login,
                password=senha
            )
            if usuario is not None:
                auth.login(request, usuario)
                next = request.GET.get("next", None)
                if next is not None:
                    return redirect(next)
                return redirect('orion:lista_home')

            
        messages.error(request, "Login ou Senha incorretos")
        return render(request, 'usuarios/pages/login.html', {'form': form})
    else:
        formLogin = LoginForm()
        contexto = {
            'form': formLogin
        }
        return render(request, 'usuarios/pages/login.html', contexto)

@login_required
def cadastro_usuario(request):
    if not request.user.is_authenticated:
        return redirect('login')
    usuario = get_object_or_404(Usuario, user_id=request.user.id)
    
    if usuario.tipo != 'A':
        messages.error(request, f"Usuário {usuario.user.username} não é Administrador")
        return redirect('orion:lista_home')


    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():

            login     = form['login'].value()
            nome      = form['nome'].value()
            sobrenome = form['sobrenome'].value()
            email     = form['email'].value()
            senha     = form['senha'].value()

            tipo_usuario = form['tipo_usuario'].value()
           
            if User.objects.filter(username=login).exists():
                messages.error(request, f"O nome {login} já foi cadastrado.")
                return render(request, 'usuarios/pages/cadastro_usuario.html',  {'form': form})

            user = User.objects.create_user(
                username=login,
                first_name = nome,
                last_name= sobrenome,
                password=senha,
                email=email
            )
            user.save()

            usuario = Usuario.objects.create(user=user, tipo=tipo_usuario)
            usuario.save()
            messages.success(request, f"Usuário {login} salvo com sucesso.")

            return redirect('usuarios:lista_usuarios')

        return render(request, 'usuarios/pages/cadastro_usuario.html',  {'form': form})

    else:
        cadastroUsuarioForm = CadastroUsuarioForm()
        contexto = {
            'form': cadastroUsuarioForm
        }
        return render(request, 'usuarios/pages/cadastro_usuario.html', contexto)

@login_required
def deletar_usuario(request, id):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')
    usuario_logado = get_object_or_404(Usuario, user_id=request.user.id)
    
    if usuario_logado.tipo != 'A':
        messages.error(request, f"Usuário {usuario_logado.user.username} não é Administrador")
        return redirect('orion:lista_home')
    try:
        user = get_object_or_404(User, pk=id)
        usuario = get_object_or_404(Usuario, user_id=id)
    except usuario.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    
    nome = usuario.user.username
    usuario.delete()
    user.delete()
    messages.success(request, f"Usuário {nome} excluido com sucesso")
    return redirect('usuarios:lista_usuarios')

@login_required(login_url="usuarios:login", redirect_field_name="next")
def dados_usuario(request):
    usuario = get_object_or_404(Usuario, user_id=request.user.id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance =request.user)
        usuarioForm = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            print("é valido")
            # Atualiza a sessão do usuário para evitar que ele seja desconectado após alterar a senha
            update_session_auth_hash(request, request.user)
            messages.success(request, "Editado com sucesso")
            return redirect('usuarios:lista_usuarios')
        
        print("não é valido")
        return render(request, 'usuarios/pages/dados_usuario.html', 
                {  'title':' Meus Dados',
                    'form': form,
                    'usuarioForm': usuarioForm  })
    else:
        userForm = UserUpdateForm(instance = request.user)
        usuarioForm = UsuarioForm(instance = usuario)
        
        if not isUserAdmin(request.user):
            usuarioForm.fields['tipo'].widget.attrs['readonly'] = True
            usuarioForm.fields['tipo'].widget.attrs['disabled'] = True

        contexto = {
            'title':' Meus Dados',
            'form': userForm,
            'usuarioForm': usuarioForm

        }
    return render(request, 'usuarios/pages/dados_usuario.html', contexto)

@login_required
def editar_usuario(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not isUserAdmin(request.user):
        messages.error(request, "Você não é administrador")
        return redirect('usuarios:lista_usuarios')

    user = get_object_or_404(User, pk = id)
    usuario = get_object_or_404(Usuario, user_id = user.id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        usuarioForm = UsuarioForm(request.POST, instance = usuario)
        
        if form.is_valid() and usuarioForm.is_valid():
            form.save()
            usuarioForm.save()
            messages.success(request, "Editado com sucesso")
            return redirect('usuarios:lista_usuarios')
        
        return render(request, 'usuarios/pages/editar_usuario.html', 
                { 'title':' Edição de Usuários',
                   'id': id,
                'form': form,
                'usuarioForm': usuarioForm
        })

    else:
        userForm = UserUpdateForm(instance = user)
        usuarioForm = UsuarioForm(instance = usuario)
        
        contexto = {
            'title':' Edição de Usuários',
            'id': id,
            'form': userForm,
            'usuarioForm': usuarioForm

        }
        return render(request, 'usuarios/pages/editar_usuario.html', contexto)

def usuario_teste(request):
    return render(request, 'usuarios/pages/usuario.html')




# usuario = Usuario.objects.select_related('user').get(pk=2)