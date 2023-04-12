import time

from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By

from apps.orion.tests.test_orion_base import OrionMixin
from apps.usuarios.tests.test_usuarios_base import UsuariosMixin
from utils.browser import make_chrome_browser


class OrionBaseFunctionalTest(LiveServerTestCase, UsuariosMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        self.browser.maximize_window()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)

    def fazer_login(self, username = "Elton", password = "@Bc123456"):
        self.make_usuario()
        self.browser.get(self.live_server_url)
        
        login_element = self.browser.find_element(By.ID, "id_login" )
        senha_element = self.browser.find_element(By.ID, "id_senha" )
        botão_element = self.browser.find_element(By.NAME, "btn_login")
        
        login_element.send_keys(username)
        senha_element.send_keys(password)
        botão_element.click()
    
    def cadastrar_empresa(self, nome = "Calebe e Gabriela Publicidade e Propaganda ME", cnpj = "82.050.804/0001-60",telefone = "1727038198", email = "auditoria@cpep.com.br", cep = "15061881", numero= "100" ):
        self.browser.get(self.live_server_url + '/empresas/')
        self.browser.find_element(By.LINK_TEXT, 'Nova Empresa').click()
        self.browser.find_element(By.ID, 'id_nome').send_keys(nome)
        self.browser.find_element(By.ID, 'id_cnpj').send_keys(cnpj)
        self.browser.find_element(By.ID, 'id_telefone').send_keys(telefone)
        self.browser.find_element(By.ID, 'id_email').send_keys(email)
        self.browser.find_element(By.ID, 'btn_adicionar_endereco').click()
        cep_input = self.browser.find_element(By.ID, 'id_cep')
        self.sleep(1)
        cep_input.send_keys(cep)
        self.browser.find_element(By.ID, 'buscaCep').click()
        self.sleep(5)
        
        self.browser.find_element(By.ID, 'id_numero').send_keys(numero)
        self.browser.find_element(By.ID, 'btn_salvar_endereco').click()
        self.browser.execute_script("window.scrollBy(0, 500)")
        self.sleep(1)
        self.browser.find_element(By.NAME, 'btn-salvar-empresa').click()
        self.sleep(1)
    
    def cadastrar_equipamento(self, empresa = "Calebe e Gabriela Publicidade e Propaganda ME", numero_serie = "84217", equipamento="Somatom Spirit", tipo_equipamento="CT"):
        self.browser.get(self.live_server_url + '/equipamentos/')
        self.browser.find_element(By.LINK_TEXT, 'Novo Equipamento').click()
        
        self.browser.find_element(By.ID, 'id_numero_serie').send_keys(numero_serie)
        self.browser.find_element(By.ID, 'id_equipamento').send_keys(equipamento)
        self.browser.find_element(By.ID, 'id_tipo_equipamento').send_keys(tipo_equipamento)

        self.browser.find_element(By.ID, 'select2-id_empresa-container').click()
        self.browser.find_element(By.XPATH, f'//*[text()="{empresa}"]').click()
        self.browser.find_element(By.XPATH, '//button[@form="form-equipamento"]').click()

       