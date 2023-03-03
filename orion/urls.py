
from django.urls import path
from django.views.i18n import JavaScriptCatalog

from orion import views

app_name = 'orion'

urlpatterns = [
     path('', views.lista_home, name='lista_home'),
     path('chamados/', views.lista_chamados, name='lista_chamados'),
     path('chamados_fechados/', views.chamados_fechados, name='chamados_fechados'),
     path('fechar_chamado/<int:id>/', views.fechar_chamado, name='fechar_chamado'),
     path('chamados/<int:id>/', views.novo_chamado_view, name='novo_chamado_view'),
     path('novo_chamado/', views.novo_chamado, name='novo_chamado'),
     path('editar_chamado/<int:id>/', views.editar_chamado, name='editar_chamado'),
     path('deletar_chamado/<int:id>/', views.deletar_chamado, name='deletar_chamado'),
     path('equipamentos/', views.equipamentos, name='equipamentos'),
     path('equipamentos/<int:id>/', views.detalhar_equipamento,
          name='detalhar_equipamento'),
     path('cadastrar_equipamentos/', views.cadastrar_equipamentos,
          name='cadastrar_equipamentos'),
     path('deletar_equipamento/<int:id>/',
          views.deletar_equipamento, name='deletar_equipamento'),
     path('clientes/', views.clientes, name='clientes'),
     path('clientes/<int:id>/', views.detalhar_cliente, name='detalhar_cliente'),
     path('deletar_cliente/',
          views.deletar_cliente, name='deletar_cliente'),
     path('cadastrar_clientes/', views.cadastrar_clientes, name='cadastrar_clientes'),
     path('teste', views.teste, name='teste'),
     path('teste_create', views.teste_create, name='teste_create'),
     path('list_teste', views.list_teste, name='list_teste'),

]
