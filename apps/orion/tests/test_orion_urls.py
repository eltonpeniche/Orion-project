import pytest
from django.test import TestCase
from django.urls import reverse

from apps.orion.models import Empresa, Endereco, Equipamento

from .test_orion_base import OrionMixin


class OrionURLsTest(TestCase, OrionMixin):
    @pytest.mark.fast
    def test_orion_home_url_esta_correta(self):
        url = reverse('orion:lista_home')
        self.assertEqual(url, '/')

    def test_orion_lista_chamados_url_esta_correta(self):
        url = reverse('orion:lista_chamados')
        self.assertEqual(url, '/chamados/')

    def test_orion_chamados_fechados_url_esta_correta(self):
        url = reverse('orion:chamados_fechados')
        self.assertEqual(url, '/chamados_fechados/')
    
    def test_orion_fechar_chamado_url_esta_correta(self):
        url = reverse('orion:fechar_chamado', kwargs = { 'id':1 })
        self.assertEqual(url, '/fechar_chamado/1/')
    
    def test_orion_novo_chamado_view_url_esta_correta(self):
        url = reverse('orion:novo_chamado_view', kwargs = { 'id':1 })
        self.assertEqual(url, '/chamados/1/')

    def test_orion_novo_chamado_url_esta_correta(self):
        url = reverse('orion:novo_chamado')
        self.assertEqual(url, '/novo_chamado/')

    def test_orion_editar_chamado_url_esta_correta(self):
        url = reverse('orion:editar_chamado', kwargs = { 'id':1 })
        self.assertEqual(url, '/editar_chamado/1/')
    
    def test_orion_deletar_chamado_url_esta_correta(self):
        url = reverse('orion:deletar_chamado', kwargs = { 'id':1 })
        self.assertEqual(url, '/deletar_chamado/1/')
    
    def test_orion_equipamentos_url_esta_correta(self):
        url = reverse('orion:equipamentos' )
        self.assertEqual(url, '/equipamentos/')

    def test_orion_detalhar_equipamento_url_esta_correta(self):
        url = reverse('orion:detalhar_equipamento', kwargs = { 'id':1 })
        self.assertEqual(url, '/equipamentos/1/')

    def test_orion_cadastrar_equipamentos_url_esta_correta(self):
        url = reverse('orion:cadastrar_equipamentos' )
        self.assertEqual(url, '/cadastrar_equipamentos/')


    def test_orion_deletar_equipamento_url_esta_correta(self):
        url = reverse('orion:deletar_equipamento', kwargs = { 'id':1 })
        self.assertEqual(url, '/deletar_equipamento/1/')

    def test_orion_cliente_url_esta_correta(self):
        url = reverse('orion:clientes')
        self.assertEqual(url, '/clientes/')

    def test_orion_deletar_cliente_url_esta_correta(self):
        url = reverse('orion:deletar_cliente')
        self.assertEqual(url, '/deletar_cliente/')

    def test_orion_cadastrar_clientes_url_esta_correta(self):
        url = reverse('orion:cadastrar_clientes')
        self.assertEqual(url, '/cadastrar_clientes/')
 

