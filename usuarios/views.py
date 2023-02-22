
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from usuarios.forms import CadastroUsuarioForm, LoginForm

from .models import Usuario


# autenticação de usuários
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    contexto = {
        'forms': usuarios,
        'titulo': 'Lista de Usuários'
    }
    return render(request, 'usuarios/pages/lista_usuarios.html', contexto)


def logout(request):
    auth.logout(request)
    messages.success(request, "Logout realizado com sucesso")
    print("Logout realizado com sucesso")
    return redirect('login')


def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form['login'].value()
            senha = form['senha'].value()
            usuario = auth.authenticate(
                request,
                username=login,
                password=senha
            )
            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f"Bem-vindo, {login} ")
                print("LOGOU")
                return redirect('lista_home')

            else:
                messages.error(request, "Login ou Senha incorretos")
                return redirect('login')
    else:
        formLogin = LoginForm()
        contexto = {
            'form': formLogin
        }
        return render(request, 'usuarios/pages/login.html', contexto)


def cadastro_usuario(request):
    if not request.user.is_authenticated:
        return redirect('login')
    usuario = get_object_or_404(Usuario, user_id=request.user.id)
    
    if usuario.tipo != 'A':
        messages.error(request, f"Usuário {usuario.user.username} não é Administrador")
        return redirect('lista_home')


    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():

            login = form['login'].value()
            email = form['email'].value()
            senha = form['senha'].value()
            senha2 = form['confirmacao_senha'].value()
            tipo_usuario = form['tipo_usuario'].value()
           
            if User.objects.filter(username=login).exists():
                messages.error(request, "Técnico já cadastrado anteriormente")
                return render(request, 'usuarios/pages/cadastro_usuario.html',  {'form': form})

            user = User.objects.create_user(
                username=login,
                password=senha,
                email=email
            )
            user.save()

            usuario = Usuario.objects.create(user=user, tipo=tipo_usuario)
            usuario.save()
            messages.success(request, f"Técnico {login} salvo com sucesso.")

            return redirect('lista_usuarios')

        return render(request, 'usuarios/pages/cadastro_usuario.html',  {'form': form})

    else:
        cadastroUsuarioForm = CadastroUsuarioForm()
        contexto = {
            'form': cadastroUsuarioForm
        }
        return render(request, 'usuarios/pages/cadastro_usuario.html', contexto)


def deletar_usuario(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    usuario_logado = get_object_or_404(Usuario, user_id=request.user.id)
    
    if usuario_logado.tipo != 'A':
        messages.error(request, f"Usuário {usuario_logado.user.username} não é Administrador")
        return redirect('lista_home')
    try:
        user = get_object_or_404(User, pk=id)
        usuario = get_object_or_404(Usuario, user_id=id)
    except usuario.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    
    nome = usuario.user.username
    usuario.delete()
    user.delete()
    messages.success(request, f"Usuário {nome} excluido com sucesso")
    return redirect('lista_usuarios')

def usuario_teste(request):
    return render(request, 'usuarios/pages/usuario.html')