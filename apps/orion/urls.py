
from django.urls import path

from apps.orion import views

app_name = 'orion'

urlpatterns = [
     path('', views.ChamadoHomeList.as_view(), name='lista_home'),
     path('chamados/', views.ChamadoList.as_view(), name='lista_chamados'),
     path('chamados/busca/', views.busca_chamados, name='busca_chamados'),
     path('chamados_fechados/', views.ChamadosFechadosList.as_view(), name='chamados_fechados'),
     path('fechar_chamado/<int:id>/', views.fechar_chamado, name='fechar_chamado'),
     path('chamados/<int:id>/', views.novo_chamado_view, name='novo_chamado_view'),
     path('novo_chamado/', views.novo_chamado, name='novo_chamado'),
     path('editar_chamado/<int:id>/', views.editar_chamado, name='editar_chamado'),
     path('deletar_chamado/<int:id>/', views.deletar_chamado, name='deletar_chamado'),
     
     path('equipamentos/', views.EquipamentoList.as_view(), name='equipamentos'),
     path('equipamentos/<int:id>/', views.EquipamentoDetail.as_view(),name='detalhar_equipamento'),
     path('equipamentos_select2/<int:id>/', views.equipamentos_select2, name='equipamentos_select2'),
     path('equipamentos/novo', views.EquipamentoDetail.as_view(), name='cadastrar_equipamentos'),
     
     path('deletar_equipamento/<int:id>/', views.EquipamentoDelete.as_view(), name='deletar_equipamento'),
     
     path('empresas/', views.empresas, name='empresas'),
     path('empresas/<int:id>/', views.detalhar_empresa, name='detalhar_empresa'),
     path('empresas/deletar/', views.deletar_empresa, name='deletar_empresa'),
     path('empresas/novo/', views.cadastrar_empresa, name='cadastrar_empresa'),
     
     path('assinatura_popup', views.assinatura_popup, name='assinatura_popup'),
     path('marcar_notificacao_como_lida', views.marcar_notificacao_como_lida, name = "marcar_notificacao_como_lida"),
     path('relatorio_ponto', views.relatorio_ponto, name = "relatorio_ponto"),
     path('download/', views.download_file, name='download_file'),
     path('teste', views.teste, name='teste'),
     path('list_teste', views.list_teste, name='list_teste'),

]
