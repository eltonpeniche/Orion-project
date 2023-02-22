from django.urls import path

from . import views

urlpatterns = [
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('deletar_usuario/<int:id>', views.deletar_usuario, name='deletar_usuario'),
    path('usuario_teste/', views.usuario_teste, name='usuario_teste'),
]
