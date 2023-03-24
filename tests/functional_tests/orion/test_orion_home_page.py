import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import OrionBaseFunctionalTest


class OrionHomePageFunctionalTest(OrionBaseFunctionalTest):

    @pytest.mark.functional_test
    def test_the_test(self):
        self.browser.get(self.live_server_url)
        self.sleep(2)
        body = self.browser.find_element(By.TAG_NAME,  'body')
        self.assertIn('Entre com o seu Login e Senha', body.text)
    
    @pytest.mark.functional_test
    def test_usuario_consegue_fazer_login_com_sucesso(self):
        self.make_login()
        body = self.browser.find_element(By.TAG_NAME,  'body')
        self.assertIn('Olá, Elton', body.text)

       
    def test_usuario_consegue_acessar_chamados_abertos(self):
        self.make_login()
        self.browser.find_element(By.NAME, 'chamado-menu').click()
        self.browser.find_element(By.XPATH, '//a[@href="/chamados/"]').click()
        body = self.browser.find_element(By.TAG_NAME,  'td')
        
        self.assertIn('Sem registros', body.text)
    
    def test_usuario_consegue_cadastrar_novo_cliente(self):
        self.make_login()
        self.browser.find_element(By.NAME, 'cadastros-menu').click()
        self.browser.find_element(By.XPATH, '//a[@href="/clientes/"]').click()
        self.browser.find_element(By.LINK_TEXT, 'Novo Cliente').click()
        
        self.browser.find_element(By.ID, 'id_nome').send_keys('Calebe e Gabriela Publicidade e Propaganda ME')
        self.browser.find_element(By.ID, 'id_cnpj').send_keys('82.050.804/0001-60')
        self.browser.find_element(By.ID, 'id_telefone').send_keys('1727038198')
        self.browser.find_element(By.ID, 'id_email').send_keys('auditoria@calebeegabrielapublicidadeepropagandame.com.br')
        self.browser.find_element(By.ID, 'btn_adicionar_endereco').click()
        cep = self.browser.find_element(By.ID, 'id_cep')
        self.sleep(1)
        cep.send_keys('15061881')
        self.browser.find_element(By.ID, 'buscaCep').click()

        self.sleep(4)
        self.browser.find_element(By.ID, 'id_numero').send_keys('100')
        self.browser.find_element(By.ID, 'btn_salvar_endereco').click()
        self.browser.execute_script("window.scrollBy(0, 500)")
        self.sleep(1)
        self.browser.find_element(By.NAME, 'btn-salvar-cliente').click()
        self.sleep(1)
        body = self.browser.find_element(By.TAG_NAME,  'body')
        self.assertIn("Novo Cliente cadastrado com sucesso.", body.text)
        