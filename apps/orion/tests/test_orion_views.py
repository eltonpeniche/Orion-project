from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import resolve, reverse

from orion import views


class OrionViewsTest(TestCase):
     def setUp(self):
          self.client = Client()
          self.user = User.objects.create_user('testuser', password='testpass')
          self.client.login(username='testuser', password='testpass')
     
     def test_orion_lista_home_view_function_is_correct(self):
          view =  resolve(reverse('orion:lista_home'))  
          self.assertIs(view.func, views.lista_home)

     def test_orion_lista_chamados_view_function_is_correct(self):
          view =  resolve(reverse('orion:lista_chamados'))  
          self.assertIs(view.func, views.lista_chamados)

     def test_orion_novo_chamado_view_view_function_is_correct(self):
          view = resolve(reverse('orion:novo_chamado_view', kwargs = { 'id':1 }))  
          self.assertIs(view.func, views.novo_chamado_view)

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
          self.assertIs(view.func, views.chamados_fechados)


     def test_orion_fechar_chamado_view_function_is_correct(self):
          view = resolve(reverse('orion:fechar_chamado', kwargs = { 'id':1 }))  
          self.assertIs(view.func, views.fechar_chamado)

     def test_orion_equipamentos_view_function_is_correct(self):
          view = resolve(reverse('orion:equipamentos'))  
          self.assertIs(view.func, views.equipamentos)

     def test_orion_detalhar_equipamento_view_function_is_correct(self):
          view = resolve(reverse('orion:detalhar_equipamento', kwargs = { 'id':1 }))  
          self.assertIs(view.func, views.detalhar_equipamento)

     def test_orion_cadastrar_equipamentos_view_function_is_correct(self):
          view = resolve(reverse('orion:cadastrar_equipamentos'))  
          self.assertIs(view.func, views.cadastrar_equipamentos)


     def test_orion_deletar_equipamento_view_function_is_correct(self):
          view = resolve(reverse('orion:deletar_equipamento', kwargs = { 'id':1 }))  
          self.assertIs(view.func, views.deletar_equipamento)

     def test_orion_clientes_view_function_is_correct(self):
          view = resolve(reverse('orion:clientes'))  
          self.assertIs(view.func, views.clientes)
          
     def test_orion_detalhar_cliente_view_function_is_correct(self):
          view = resolve(reverse('orion:detalhar_cliente', kwargs = { 'id':1 }))  
          self.assertIs(view.func, views.detalhar_cliente)

     def test_orion_deletar_cliente_view_function_is_correct(self):
          view = resolve(reverse('orion:deletar_cliente'))  
          self.assertIs(view.func, views.deletar_cliente)

     def test_orion_lista_home_view_return_status_code_200_ok(self):
          response = self.client.get(reverse('orion:lista_chamados'))
          self.assertEqual(response.status_code, 200)
