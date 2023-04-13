import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import resolve, reverse

from apps.orion import views
from apps.orion.models import Chamado, Empresa, Equipamento
from apps.orion.tests.test_orion_base import OrionMixin


@pytest.mark.fast
class OrionViewsTest(TestCase, OrionMixin):
     def setUp(self):
          self.client = Client()
          self.user = User.objects.create_user(username='testuser', password='testpass')
          self.client.login(username='testuser', password='testpass')
     
     def test_orion_lista_home_view_function_is_correct(self):
          view =  resolve(reverse('orion:lista_home'))  
          self.assertIs(view.func.view_class, views.ChamadoHomeList)
     
     def test_orion_lista_home_view_loads_correct_template(self):
          response = self.client.get(reverse('orion:lista_chamados'))
          self.assertTemplateUsed(response, 'orion/pages/chamado_list.html')

     def test_orion_lista_chamados_template_loads_chamados(self):
          self.make_chamado()
          response = self.client.get(reverse('orion:lista_chamados')) 
          self.assertIn("Chamado de Teste", response.content.decode('utf-8'))
     
     def test_orion_lista_chamados_dont_loads_chamados_fechados(self):
          self.make_chamado(status_chamado = "F")
          response = self.client.get(reverse('orion:lista_chamados')) 
          self.assertIn("Sem registros", response.content.decode('utf-8'))
     
     def test_orion_lista_chamados_view_function_is_correct(self):
          view =  resolve(reverse('orion:lista_chamados'))  
          self.assertIs(view.func.view_class, views.ChamadoList)
     

     def test_orion_novo_chamado_view_view_function_is_correct(self):
          view = resolve(reverse('orion:novo_chamado_view', kwargs = { 'id':1 }))  
          self.assertIs(view.func, views.novo_chamado_view)

     def test_orion_novo_chamado_view_return_status_code_200_ok(self):
          response = self.client.get(reverse('orion:novo_chamado_view', kwargs = { 'id':1 }))
          self.assertEqual(response.status_code, 200)
     
     def test_orion_novo_chamado_view_loads_correct_template(self):
          response = self.client.get(reverse('orion:novo_chamado_view', kwargs = { 'id':1 }))
          self.assertTemplateUsed(response, 'orion/pages/novo_chamado.html')

     def test_orion_novo_chamado_view_function_is_correct(self):
          view = resolve(reverse('orion:novo_chamado'))  
          self.assertIs(view.func, views.novo_chamado)


     def test_orion_editar_chamado_view_function_is_correct(self):
          view = resolve(reverse('orion:editar_chamado', kwargs = { 'id':1 }))  
          self.assertIs(view.func, views.editar_chamado)

     def test_orion_deletar_chamado_view_function_is_correct(self):
          view = resolve(reverse('orion:deletar_chamado', kwargs = { 'id':1 }))  
          self.assertIs(view.func, views.deletar_chamado)

     def test_orion_chamados_fechados_view_function_is_correct(self):
          view = resolve(reverse('orion:chamados_fechados'))  
          self.assertIs(view.func.view_class, views.ChamadosFechadosList)


     def test_orion_fechar_chamado_view_function_is_correct(self):
          view = resolve(reverse('orion:fechar_chamado', kwargs = { 'id':1 }))  
          self.assertIs(view.func, views.fechar_chamado)

     def test_orion_equipamentos_view_function_is_correct(self):
          view = resolve(reverse('orion:equipamentos'))  
          self.assertIs(view.func.view_class, views.EquipamentoList)

     def test_orion_detalhar_equipamento_view_function_is_correct(self):
          view = resolve(reverse('orion:detalhar_equipamento', kwargs = { 'id':1 }))  
          self.assertIs(view.func.view_class, views.EquipamentoDetail)

     def test_orion_cadastrar_equipamentos_view_function_is_correct(self):
          view = resolve(reverse('orion:cadastrar_equipamentos'))  
          self.assertIs(view.func.view_class, views.EquipamentoDetail)


     def test_orion_deletar_equipamento_view_function_is_correct(self):
          view = resolve(reverse('orion:deletar_equipamento', kwargs = { 'id':1 }))  
          self.assertIs(view.func.view_class, views.EquipamentoDelete)

     def test_orion_empresas_view_function_is_correct(self):
          view = resolve(reverse('orion:empresas'))  
          self.assertIs(view.func, views.empresas)
          
     def test_orion_detalhar_empresas_view_function_is_correct(self):
          view = resolve(reverse('orion:detalhar_empresa', kwargs = { 'id':1 }))  
          self.assertIs(view.func, views.detalhar_empresa)

     def test_orion_deletar_empresas_view_function_is_correct(self):
          view = resolve(reverse('orion:deletar_empresa'))  
          self.assertIs(view.func, views.deletar_empresa)

