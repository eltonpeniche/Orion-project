import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import UsuariosBaseFunctionalTest


class UsuariosFunctionalTest(UsuariosBaseFunctionalTest):

    def test_form_em_branco_consegue_fazer_login(self):
        self.make_usuario()
        
        username = " "
        password = " "
        
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, "id_login" ).send_keys(username)
        self.browser.find_element(By.ID, "id_senha" ).send_keys(password)
        self.browser.find_element(By.NAME, "btn_login").click()
        message = self.browser.find_element(By.XPATH, '//div[@class="alert alert-danger"]')
        self.assertIn('Login ou Senha incorretos', message.text)

    def test_usuario_invalido_consegue_fazer_login(self):
        self.make_usuario()
        
        username = "Elton"
        password = "$Bc123456"
        
        self.browser.get(self.live_server_url)
        
        self.browser.find_element(By.ID, "id_login" ).send_keys(username)
        self.browser.find_element(By.ID, "id_senha" ).send_keys(password)
        self.browser.find_element(By.NAME, "btn_login").click()
        message = self.browser.find_element(By.XPATH, '//div[@class="alert alert-danger"]')
        self.assertIn('Login ou Senha incorretos', message.text)
    
    @pytest.mark.functional_test
    def test_usuario_consegue_fazer_login_com_sucesso(self):
        self.fazer_login()
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Olá, Elton', body.text)
