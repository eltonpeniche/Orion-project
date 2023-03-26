import time

from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By

from apps.usuarios.tests.test_usuarios_base import UsuariosMixin
from utils.browser import make_chrome_browser


class UsuariosBaseFunctionalTest(LiveServerTestCase, UsuariosMixin):
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
    

       