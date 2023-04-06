import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import OrionBaseFunctionalTest


class OrionFunctionalTest(OrionBaseFunctionalTest):

    @pytest.mark.functional_test
    def test_the_test(self):
        print(self.live_server_url)
        self.browser.get(self.live_server_url)
        self.sleep(10)
        body = self.browser.find_element(By.TAG_NAME,  'body')
        self.assertIn('Entre com o seu Login e Senha', body.text)
    

    @pytest.mark.functional_test
    def test_usuario_consegue_acessar_chamados_abertos(self):
        self.browser.get(self.live_server_url + '/chamados/')
        self.fazer_login()
        body = self.browser.find_element(By.TAG_NAME,  'td')
        self.assertIn('Sem registros', body.text)
      
    def test_usuario_consegue_cadastrar_novo_cliente(self):
        self.fazer_login()
        self.cadastrar_empresa()
        message = self.browser.find_element(By.XPATH, '//div[@class="alert alert-success"]')
        self.assertIn("Novo Cliente cadastrado com sucesso.", message.text)
    
    @pytest.mark.functional_test
    def test_usuario_consegue_cadastrar_novo_equipamento(self):
        self.fazer_login()
        self.cadastrar_empresa(nome = "Gabriela Publicidade e Propaganda ME", cnpj = "82.050.804/0001-60",telefone = "1727038198", email = "auditoria@cpep.com.br", cep = "15061881", numero= "101")
        self.cadastrar_empresa()
        self.cadastrar_equipamento()
        message = self.browser.find_element(By.XPATH, '//div[@class="alert alert-success"]')
        self.assertIn("Novo equipamento cadastrado com sucesso", message.text)
        