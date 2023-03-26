import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import UsuariosBaseFunctionalTest


class OrionHomePageFunctionalTest(UsuariosBaseFunctionalTest):

    @pytest.mark.functional_test
    def test_usuario_consegue_fazer_login_com_sucesso(self):
        self.fazer_login()
        body = self.browser.find_element(By.TAG_NAME,  'body')
        self.assertIn('Olá, Elton', body.text)
